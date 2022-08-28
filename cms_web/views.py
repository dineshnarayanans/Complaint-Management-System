from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import auth,User
from django.contrib.auth.decorators import login_required
from .models import Profile,Complaint,Notification,Feedback, Subordinate


# Create your views here.
def home(request):
    user = request.user
    return render(request,'index.html',{'user':user})

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        username=email
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('signup')
            else:   
                user = User.objects.create_user(username=username, password=password1, email=email,first_name=first_name,last_name=last_name)
                user.save()
                messages.success(request,'account created, please create profile')
                auth.login(request,user)
                return redirect('profile')

        else:
            messages.info(request,'password not matching..')    
            return redirect('signup')
            
    else:
        return render(request,'signup.html')


def login(request):
    user = request.user
    if user.is_authenticated:
        messages.info(request,'already logged in')
        return redirect("/")
    if request.method== 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            messages.success(request,'login successful')
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request,'Invalid credentials')
            return redirect('login')
    else:
        return render(request,'login.html')

@login_required
def profile(request):
    user = request.user
    if Profile.objects.filter(user=user.id).exists():
        return render(request,'profile.html',{'user':user})

    elif request.method == 'POST' :
        ada = request.POST['adhaar']
        dob = request.POST['dob']
        phone = request.POST['phone']
        photo = request.FILES.get('photo','photo/default.jpg')
        Profile.objects.create(user=user,adhaar_no=ada,dob=dob,phone=phone,photo=photo)
        messages.info(request,'profile create')
        return render(request,'profile.html',{'user':user})
    else:
        return render(request,'profile.html')

def logout(request):
    auth.logout(request)
    messages.info(request,'you have been logged out')
    return redirect("/")

@login_required
def complaint(request):
    user = request.user
    if request.method == 'POST':
        title = request.POST['title']
        file = request.FILES['file']
        complain = request.POST['note']
        Complaint.objects.create(user=user,title=title,complain=complain,pic=file)
        messages.info(request,'complaint added')
        return redirect('home')
    else:
        return render(request,'complaint.html')

@login_required
def notification(request):
    user = request.user
    notifications = Notification.objects.filter(user_id=user).order_by('-created_date')
    return render(request,'notification.html',{'notifications':notifications})

@login_required
def feedback(request):
    user = request.user
    replied_fb = Feedback.objects.filter(user_id=user)
    if request.method == 'POST':
        subject = request.POST['subject']
        feedback = request.POST['feedback']
        Feedback.objects.create(user_id=user,subject=subject,feedback=feedback)
        messages.success(request,'Thank you for providing Feedback')
        return redirect("/")   
    return render(request,'feedback.html',{'replied_fb':replied_fb})


def subordinate(request):
    user = request.user
    if  Subordinate.objects.filter(subordinate=user.id).exists():
        complaints = Subordinate.objects.filter(subordinate_id=user.id)
        return render(request,'subordinate.html',{'complaints':complaints})
    elif user.is_authenticated and not user.is_staff:
        messages.info(request,'Permission denied. Your are a not subordinate')
        return redirect('/')
    elif request.method== 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None and user.is_staff:
            auth.login(request, user)
            complaints = Subordinate.objects.filter(subordinate=user.id)
            return render(request,'subordinate.html',{'complaints':complaints})
            
        else:
            messages.info(request,'Invalid credentials for subordinate login')
            return redirect('subordinate')
    return render(request,'subordinate.html')

def about(request):
    return render(request,'about.html')    
def contact(request):
    return render(request,'contact.html')
