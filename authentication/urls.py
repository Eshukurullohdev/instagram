from django.urls import path

from. import views

urlpatterns = [
    path("register/", views. register_page, name='register'),
    path("login/", views. login_page, name='login'),
    path("forget_password/",views.  forget_password_page, name='forget_password'),
    path("step/", views.StepView.as_view(), name="step"),
    path("step_second/", views. StepView.as_view(), name="step_second"),
    path("step_third/", views. ThirdStepView.as_view(), name="step_third"),
    path("help_center/", views. help_Center_page, name="help_center"),
    path("user_profile/<str:username>/", views.Profile_page.as_view(), name="profile"),
    path("update_profile/<int:pk>/", views. profileUpdateView.as_view(), name="update_profile"),
    path("request-friend/<int:id>/", views.request_friend),
    path("notifications/", views.Notification.as_view(), name="notification"),
    path("add-to-friend/<int:id>/<int:friend_request_id>/", views.accept_friend)
]

# http://127.0.0.1:8000/authentication/request-friend/5