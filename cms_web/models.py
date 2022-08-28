from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    adhaar_no = models.CharField(max_length=13)
    dob = models.DateField()
    phone = models.CharField(max_length=11)
    photo = models.ImageField(default='photo/default.jpg',upload_to='photo')
    def __str__(self):
        return str(self.user)
    

class  Complaint(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=25)
    created_at = models.DateField(default=date.today)
    complain = models.TextField(max_length=200)
    status = models.CharField(max_length=20,choices=(('P','Pending'),('C','Completed')),default='P')
    pic = models.FileField(upload_to='complaint_files')
    def __str__(self):
        return self.title

class Notification(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    type = models.CharField(max_length=30)
    message = models.TextField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.user_id) + str(self.type)

class Feedback(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=30)
    feedback = models.TextField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    reply = models.TextField(max_length=60,blank=True)
    def __str__(self):
        return str(self.user_id) + ":" + self.subject

class Subordinate(models.Model):
    subordinate = models.OneToOneField(User,on_delete=models.CASCADE)
    complaint = models.ForeignKey(Complaint,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.complaint.title)