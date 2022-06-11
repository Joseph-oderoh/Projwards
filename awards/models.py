from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.


class Project(models.Model):
    """
    This class takes care of the posted projects
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')

    image = CloudinaryField('image')
    title = models.CharField(max_length=50)
    description=models.CharField(max_length=100)
    url = models.TextField()
    posted_date = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(default=0)

    @classmethod
    def get_project_by_user(cls, user):
        project = cls.objects.filter(user=user)
        return project

    def save_project(self):
        self.save()

    def delete_project(self):
        self.delete()

    #  get by id
    @classmethod
    def get_one_project(cls, id):
        project = cls.objects.get(id=id)
        return project

    
    @classmethod
    def search_by_title(self, search_title):
        
        projects = Project.objects.filter(title__icontains=search_title)
        return projects
  

    def __str__(self):
        return self.title      


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_photo = CloudinaryField('image')
    bio = models.TextField(max_length=500, default="Your Bio", blank=True)
    name = models.CharField(blank=True, max_length=120)
    location = models.CharField(max_length=60, blank=True)
    contact = models.EmailField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()