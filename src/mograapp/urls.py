from django.urls import path
from . import views

urlpatterns = [
    path('',views.mografunction),
    path('mogra/', views.mografunction),
]
