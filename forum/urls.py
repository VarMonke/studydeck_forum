from django.urls import path
from . import views

urlpatterns = [
    path("", views.thread_list, name="thread_list"),
    path("<int:thread_id>/", views.thread_detail, name="thread_detail"),
    path("<int:thread_id>/reply/", views.add_reply, name="add_reply"),
    path("new/", views.create_thread, name="create_thread"),
    path("vote/<str:kind>/<int:obj_id>/<str:direction>/",views.vote,name="vote"),
    path("report/", views.report, name="report"),
    path("report/<str:target_type>/<int:target_id>/",views.report_form,name="report_form",),
]