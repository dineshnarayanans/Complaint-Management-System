from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('login', views.login,name='login'),
    path('profile', views.profile,name='profile'),
    path('signup', views.signup,name='signup'),
    path('logout',views.logout,name='logout'),
    path('complaint',views.complaint,name='complaint'),
    path('notification',views.notification,name='notification'),
    path('feedback',views.feedback,name='feedback'),
    path('subordinate',views.subordinate,name='subordinate'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact')
]