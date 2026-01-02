from django.urls import path
from . import views

urlpatterns = [
    path("reply/<int:reply_id>/delete/", views.delete_reply, name="delete_reply"),
    path("thread/<int:thread_id>/lock/", views.lock_thread, name="lock_thread"),
    path("user/<int:user_id>/ban/", views.ban_user, name="ban_user"),
]