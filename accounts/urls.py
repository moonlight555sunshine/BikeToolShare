from django.urls import path
from accounts.views import RegisterView, LoginView, LogoutView, UpdateInfoView, AccountView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update_info', UpdateInfoView.as_view(), name='update_info'),
    path('account/', AccountView.as_view(), name='account'),

]