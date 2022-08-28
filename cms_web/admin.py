from django.contrib import admin
from . models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Complaint)
admin.site.register(Notification)
admin.site.register(Feedback)
admin.site.register(Subordinate)