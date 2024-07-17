from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.Signup.as_view(), name='signup'),
    path('activate/<uid64>/<token>',views.activate, name="activate"),

    # Add more paths as needed
]
