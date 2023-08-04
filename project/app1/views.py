from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import MRIImage  # Import the model for MRIImage
@login_required(login_url='login')

def HomePage(request):
    if request.method == 'POST':
        # Check if the form is valid (i.e., an image is uploaded)
        if 'image' in request.FILES:
            # Get the uploaded image and username from the form
            uploaded_image = request.FILES['image']
            username = request.user.username  # Get the current user's username

            # Save the image and username to the database
            mri_image = MRIImage.objects.create(image=uploaded_image, username=username)

            # Optionally, you can perform some additional actions or redirect the user to another page
            return render (request,'upload.html')  # Replace 'success_url' with the URL you want to redirect to after successful upload

    return render(request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        



    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')