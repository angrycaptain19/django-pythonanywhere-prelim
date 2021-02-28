from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#what does Todo consist of
class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True) #someone doesnt have to fill up the memo if they dont want to, use case: grocery list
    created = models.DateTimeField(auto_now_add=True) #auto_now_add, instantly specify the particular time it was created
    datecompleted = models.DateTimeField(null=True, blank=True) #give it an opportunity to be null and specify the time later
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    #makemigrations after setting up the model
    #migrate the database

    #then go to admin.py

    def __str__(self):
        return f"{self.title} ----| Created: {self.created.strftime('%m/%d/%Y')}"
