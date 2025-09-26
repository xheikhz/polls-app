import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin

class Books(models.Model):
    bookname=models.CharField(max_length=50)
    price=models.FloatField(max_length=10)
    
class Questions(models.Model):
    question_text=models.CharField(max_length=200)
    pub_date=models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    
    @admin.display(
            boolean=True,
            ordering='pub_date',
            description='Published recently?',
    )
    def was_publishedrecently(self):
        now=timezone.now()
        return now-datetime.timedelta(days=1)<=self.pub_date<=now
        
    
class Choice(models.Model):
    question=models.ForeignKey("Questions",on_delete=models.CASCADE)
    choice_field=models.CharField(max_length=200)
    votes=models.IntegerField(default=0)
    def __str__(self):
        return self.choice_field
    