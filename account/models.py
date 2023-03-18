from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(default='default.jpg', upload_to='users/%Y/%m/%d', blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save()
        if self.profile_picture:
            img = Image.open(self.profile_picture.path)
            if img.height > 180 or img.width > 180:
                output_size = (180, 180)
                img.thumbnail(output_size)
                img.save(self.profile_picture.path)
                

class Contact(models.Model):
    userFrom = models.ForeignKey(User, on_delete=models.CASCADE, related_name='relFromSet')
    userTo = models.ForeignKey(User, on_delete=models.CASCADE, related_name='relToSet')
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return '{} follows {}'.format(self.userFrom, self.userTo)
 
    
"""
Add this field to the built in 'User' table dynamically.
The field is called the 'following'
The field is looked like this:-
following = models.ManyToManyField('self',through=Contact, related_name='followers', symmetrical=False)
"""
userModel = get_user_model()
userModel.add_to_class('following', models.ManyToManyField('self', through=Contact, related_name='followers', symmetrical=False))