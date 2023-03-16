from django.urls import path
from . import views



urlpatterns = [
    path('',views.MograView.as_view(), name='mogra'),
    path('signup/', views.MySignupView.as_view(), name='signup'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', views.MyLogoutView.as_view(next_page='/login/'), name='logout'),
    path('mypage/', views.MyUserView.as_view(), name='mypage'),
    path('event/<uuid:uuid>/', views.EventDetailView.as_view(), name='event_detail'),
    path('create/',views.MyEventCreateView.as_view(),name='create'),
    path('delete/<uuid:pk>',views.DetailDeleteView.as_view(),name='delete'),
    path('update/<uuid:pk>/',views.DetailUpdateView.as_view(), name='update'),
    path('home/',views.MyGraphView.as_view(),name='home'),
    path('passwordup/',views.ChangePasswordView.as_view(), name='passwordup'),
    path('nameup/',views.ChangeUsernameView.as_view(),name='nameup'),
    path('emailup/',views.ChangeEmailView.as_view(),name='emailup'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

