
from django.db import models
from acc.models import User

# Create your models here.
class Book(models.Model):
    site_name=models.CharField(max_length=100,blank=True)
    site_url=models.TextField()
    content=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="user")
    impo=models.BooleanField(default=False)
    pubdate=models.DateTimeField()
    def __str__(self):
        return f"[{self.site_name}]"