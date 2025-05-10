from django.db import models
from django.contrib.auth.models import User
import shortuuid

# Create your models here.
class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128, unique=True, default=shortuuid.uuid) # Unique group name, default to a short UUID
    users_online = models.ManyToManyField(User, related_name='online_in_groups',blank=True) # Many-to-many relationship with User model
    members = models.ManyToManyField(User, related_name='chat_groups',blank=True) # Many-to-many relationship with User model
    is_private = models.BooleanField(default=False) # Boolean field to indicate if the group is private
    
    def __str__(self):
        return self.group_name
    

class GroupMessages(models.Model):
    group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE) # Cascade delete messages if group is deleted
    author = models.ForeignKey(User,on_delete=models.CASCADE) # Cascade delete messages if user is deleted
    body = models.TextField(max_length=300) # Message body
    created = models.DateTimeField(auto_now_add=True) # Timestamp when message was created

    def __str__(self):
        return f"{self.author.username} : {self.body}"
    
    class Meta:
        ordering = ['-created']