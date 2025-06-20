from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only authenticated users who are participants of the conversation
    to send, view, update, and delete messages.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # For Conversation objects
        if hasattr(obj, 'participants'):
            if request.method in ['PUT', 'PATCH', 'DELETE']:
                return request.user in obj.participants.all()
            return request.user in obj.participants.all()
        # For Message objects
        if hasattr(obj, 'conversation'):
            if request.method in ['PUT', 'PATCH', 'DELETE']:
                return request.user in obj.conversation.participants.all()
            return request.user in obj.conversation.participants.all()
        return False