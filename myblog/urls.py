from django.urls import path

from .views import *

urlpatterns = [
    path('home/', blogHomePage, name="home"),
    path('publish/', processWriteBlogPage, name="postBlog"),
    path('post-blog/', saveBlog, name="save-post"),
    path('signup/', userSignup, name="signup"),
    path('login/', userlogin, name="login"),
    path('forgot-password/', forgot_password, name="forgot_password"),
    path('verify-otp/', create_new_pass, name="verify_otp"),
    path('change-password/', change_password, name="change_password"),
    path('logout/', userlogout, name="logout"),
    path('blog/<int:id>/', fetchBlogPost, name="view-blog"),
    path('user/<int:id>/', viewProfile, name="profile"),
    path('user/<int:id>/update/', updateProfile, name="update_profile"),
    path('about-us/', viewAboutUs, name="aboutUsPage")
]
