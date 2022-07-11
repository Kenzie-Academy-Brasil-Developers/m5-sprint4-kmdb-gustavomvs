from django.urls import path
from .views import GetUser, ListUsers, RegisterView, LoginView

urlpatterns = [
    path('users/register/', RegisterView.as_view()),
    path('users/login/', LoginView.as_view()),
    path('users/', ListUsers.as_view()),
    path('users/<int:user_id>/', GetUser.as_view())
]