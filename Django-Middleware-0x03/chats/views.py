from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation, IsSenderOfMessage
from django.utils import timezone

import django_filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

class MessagePagination(PageNumberPagination):
    page_size = 20  # Set pagination size to 20
    page_size_query_param = 'page_size'
    max_page_size = 100  # Set a maximum page size


class MessageFilter(django_filters.FilterSet):
    # Filter messages by participant user
    user = django_filters.ModelChoiceFilter(queryset=User.objects.all(), field_name='conversation__participants')

    # Filter messages by date range
    start_date = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr='gte', label="Start Date")
    end_date = django_filters.DateTimeFilter(field_name="send_at", lookup_expr='lte', label="End Date")

    class Meta:
        model = Message
        fields = ['user', 'start_date', 'end_date']

class ConversationViewSet(viewsets.ModelViewSet):
    # queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        """
        Filter conversations to show only those where the user is a participant.
        """
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        participants = request.data.get('participants', [])
        # using filters
        filters = participants
        participants = User.objects.filter(user_id__in=[participant for participant in participants])

        if len(set(filters)) != len(set(participants)):
            return Response({'participants': 'Conversations cannot have duplicate participants.'}, status=status.HTTP_400_BAD_REQUEST)

        if len(set(participants)) < 2:
            return Response({'participants': 'Conversations must have at least 2 participants.'}, status=status.HTTP_400_BAD_REQUEST)
        
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    # queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsSenderOfMessage]
    pagination_class = MessagePagination
    filter_backends = (DjangoFilterBackend,)  # Using django-filters
    filterset_class = MessageFilter  # Applying the filter class

    def get_queryset(self):
        """
        Filter messages to only include those from conversations the user is part of.
        """
        # lookup + _pk (because of nestedrouter) => is equivalent to conversation_id in the url
        conversation = Conversation.objects.filter(conversation_id=self.kwargs.get("conversation_pk")).first()
        return conversation.messages if conversation else []

    def create(self, request, *args, **kwargs):
        conversation_id = kwargs.get('conversation_pk')
        conversation = Conversation.objects.get(conversation_id=conversation_id)
        sender = User.objects.get(user_id=request.data['user_id'])
        message_body = request.data['message_body']

        if not conversation:
            return Response({'conversation': 'Invalid conversation ID.'}, status=status.HTTP_400_BAD_REQUEST)

        if sender not in conversation.participants.all(): # already checked in IsSenderOfMessage
            return Response({'sender': 'User is not a participant of the conversation.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not message_body:
            return Response({'message_body': 'Message body cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(conversation=conversation, sender=sender, message_body=message_body)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
