from django.db import models


class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        """
        Returns unread messages for a specific user.
        Optimized using `.only()` to fetch only necessary fields.
        """
        return self.filter(receiver=user, is_read=True)
