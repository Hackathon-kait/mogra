from django.urls import path
from . import views

urlpatterns = [
    path('',views.MySignupView.as_view(), name='signup'),
    path('mogra/', views.mografunction),
    path('signup/', views.MySignupView.as_view(), name='signup'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('home/', views.MyUserView.as_view(), name='home'),
    path('event/<uuid:uuid>/', views.EventDetailView.as_view(), name='event_detail'),
]
