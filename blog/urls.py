from django.urls import path

from . import views

app_name="blog"
urlpatterns=[
    path("index/", views.index, name="index"),
    #path("index/detail/", views.detail, name="detail"),
    #path("index/detail",views.display2,name="detail"),
    path("index/post/<str:post_id>",views.detail,name="detail"),
    # path("new_new_url",views.new_url_view,name="new"),
    # path("old_url/",views.old_url_redirect,name="old_url")
    path("index/contact",views.contact_view,name="contact"),
    path("index/about",views.about_view,name="about"),
    path("register",views.register,name='register'),
    path("login",views.login,name='login'),
    path("dashboard",views.dashboard,name='dashboard'),
    path("logout",views.logout,name='logout'),
    path("forget_password",views.forget_password,name='forget_password'),
    path("reset_password/<uidb64>/<token>", views.reset_password, name="reset_password" ),
    path("new_post/",views.new_post,name='new_post')
]