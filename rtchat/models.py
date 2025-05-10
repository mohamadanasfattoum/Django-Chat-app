from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128, unique=True) # Unique group name
    users_online = models.ManyToManyField(User, related_name='online_in_groups',blank=True) # Many-to-many relationship with User model


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