from django.shortcuts import render
from .models import *
from django.contrib import messages
from .Supabase.supabase import upload_to_cloud
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
import random
from django.http import JsonResponse






import random

def userSignup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            return JsonResponse({"success": False, "message": "Email already exists"})
        styles = ["adventurer", "bottts", "fun-emoji", "croodles", "big-smile"]
        chosen_style = random.choice(styles)

        avatar_url = f"https://api.dicebear.com/7.x/{chosen_style}/svg?seed={username}"

        try:
            newUser = User.objects.create_user(
                email=email,
                username=username,
                password=password
            )
            newUser.avatar = avatar_url    
            newUser.save()

            return JsonResponse({"success": True, "message": "Signup successful!"})

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Invalid method"})



def userlogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        print(f"email: {email}  password: {password}")

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, email=user_obj.email, password=password)
            print("user", user)
            
            if user is not None:
                login(request, user)
                return JsonResponse({"success": True, "message": "Login successful!"})
            else:
                return JsonResponse({"success": False, "message": "Invalid password"})
        except User.DoesNotExist:
             return JsonResponse({"success": False, "message": "User does not exist"})

    return JsonResponse({"success": False, "message": "Invalid request"})


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({"success": False, "message": "User with this email does not exist"})

        otp = random.randint(1000, 9999)
        request.session["reset_otp"] = otp
        request.session["reset_email"] = email

        send_mail(
            "Reset Password",
            f"Your OTP to reset password is {otp}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )
        print(f"OTP sent: {otp}") 

        return JsonResponse({"success": True, "message": "OTP sent to email"})

    return JsonResponse({"success": False, "message": "Invalid request"})


def create_new_pass(request):
    if request.method == "POST":
        otp = request.POST.get("OTP") 
        session_otp = str(request.session.get("reset_otp"))

        if not session_otp:
            return JsonResponse({"success": False, "message": "OTP expired. Please try again."})

        if str(otp) == session_otp:
            return JsonResponse({"success": True, "message": "OTP Verified"})
        else:
            return JsonResponse({"success": False, "message": "Incorrect OTP"})

    return JsonResponse({"success": False, "message": "Invalid request"})


def change_password(request):
    if request.method == "POST":
        new_password = request.POST.get("new_password")
        email = request.session.get("reset_email")

        if not email:
            return JsonResponse({"success": False, "message": "Session expired"})

        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            
            # Clear session
            del request.session["reset_otp"]
            del request.session["reset_email"]
            
            return JsonResponse({"success": True, "message": "Password changed successfully"})
        except Exception as e:
            return JsonResponse({"success": False, "message": "Error changing password"})

    return JsonResponse({"success": False, "message": "Invalid request"})



def userlogout(request):
    logout(request)
    return redirect("home")



def updateProfile(request, id):
    if request.method == "POST":

        print("we entered")
        user = User.objects.get(id=id)

        user.username = request.POST.get("username") 
        user.description = request.POST.get("description")

        print(f"userName: {user.username}, description: {user.description}")
        user.save(update_fields=["username", "description"])


        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "message": "Invalid method"})




 
def saveBlog(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        image = request.FILES.get("image")

        if not image:
            return JsonResponse({"success": False, "message": "Cover image is required"})


        supabase_url = upload_to_cloud(image)


        Blog_post = Blog.objects.create(
            title=title,
            content=content,
            image=supabase_url,  
            author=request.user
        )
        print("Blog_post", Blog_post)

        return JsonResponse({"success": True, "message": "Post created"})
    
    return JsonResponse({"success": False, "message": "Invalid request"})


def fetchBlogPost(request, id):
    try:
        blogPost = Blog.objects.get(id=id)
        other_posts = Blog.objects.exclude(id=id).order_by('?')[:3]
    except Blog.DoesNotExist:
        return JsonResponse({"success": False, "message": "Blog Post does not exist"})
    print(f"title: {blogPost.title}, blogimage: {blogPost.image}, blogContent: {blogPost.content}")
    return render(request, "blogView.html", {"blog": blogPost, "suggestions": other_posts})
        


def processWriteBlogPage (request):
    return render(request, "writepost.html")


def blogHomePage (request):
    allposts = Blog.objects.all().order_by("-created_at")
    for post in allposts:
        print(f"ID: {post.id}, Title: {post.title}, Created At: {post.created_at}")
    return render(request, "index.html", {"posts": allposts})



def viewProfile(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return JsonResponse({"success": False, "message": "User does not exist"})

    return render(request, "profilePage.html", {"user": user})


def viewAboutUs (request):
    return render(request, "aboutUs.html")

