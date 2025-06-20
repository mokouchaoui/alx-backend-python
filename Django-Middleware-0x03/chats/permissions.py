from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow only participants of a conversation to access it.
    """

    def has_permission(self, request, view):
        # Ensure the user is authenticated before checking object-level permission
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant of the conversation
        return request.user in obj.participants.all()


class IsSenderOfMessage(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and request.user == obj.sender

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
