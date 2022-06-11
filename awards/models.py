from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
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
        return self.user.username       
