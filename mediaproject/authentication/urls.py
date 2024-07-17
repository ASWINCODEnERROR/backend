from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.Signup.as_view(), name='signup'),

    # Add more paths as needed
]
