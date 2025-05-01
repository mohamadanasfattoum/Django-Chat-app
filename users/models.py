from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/', default=static('images/avatar.png'),null=True, blank=True)
    displayname = models.CharField(max_length=100, null=True, blank=True)
    info = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.user)
    
    @property
    def name(self):
        if self.displayname:
            return self.displayname
        else:
            return self.user.username


