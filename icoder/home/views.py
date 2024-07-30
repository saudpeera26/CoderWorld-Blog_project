from django.shortcuts import render,HttpResponse,redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from blog.models import Post

# Html Pages.
def home(request):
    return render(request,('home/home.html'))


def About(request):
    return render(request,'home/about.html')


def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']
        print(name,email,phone,content)
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, 'Plzz fill the from Correctly...')
        else:
            contact=Contact(name=name,email=email,phone=phone,content=content)
            contact.save()
            messages.success(request, 'Your msg has been successfully sent..')
    return render(request,('home/contact.html'))



def Search(request):
    querry=request.GET['querry']
    if len(querry)>78:
        allpost=Post.objects.none()
    else:
        allpostTitle=Post.objects.filter(Title__icontains=querry)
        allpostcontent=Post.objects.filter(content__icontains=querry)
        allpost= allpostTitle.union(allpostcontent)

    if allpost.count()==0:
        messages.warning(request, " no search results found. Please refine your querry")
    params={"allpost":allpost,
            "querry":querry
            }
    return render(request, "home/search.html",params)


# Authentication APIs
def handleSignup(request):
    if request.method=="POST":
        #Get the post parameters
        username=request.POST["username"]
        fname=request.POST["fname"]
        lname=request.POST["lname"]
        email=request.POST["email"]
        pass1=request.POST["pass1"]
        pass2=request.POST["pass2"]
        #check errorneous input()
        if len(username) > 10:
            messages.error(request, "username must be under 10 characters")
            return redirect("home")
        if username.isalnum():
            messages.error(request, "username should only contain letter and number")
            return redirect("home")
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect("home")
        
        myuser=User.objects.create_user(username, email, pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,"your account has been successfully created")
        return redirect("home")
    else:
        return HttpResponse("404 - Not Found...")
    


def handlelogin(request):
    loginusername=request.POST["loginusername"]
    loginpassword=request.POST["loginpassword"]
    user=authenticate(username=loginusername,password=loginpassword)

    if user is not None:
        login(request,user)
        messages.success(request, "successfully logged In")
        return redirect("home")
    else:
        messages.error(request,"Invalid Credentials, Plzz try again")
        return redirect("home")
    return HttpResponse("404 -  Not Found")



def handlelogout(request):
    logout(request)
    messages.success(request,"Successfully logged out")
    return redirect("home")
    return HttpResponse("handlelogout")