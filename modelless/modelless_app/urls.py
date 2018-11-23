from django.urls import path
from . import views

app_name = "modelless_app"
urlpatterns = [
    path('', views.Home,name='home'),
    path('register/', views.user_registration, name='register'),
    path('get_users/', views.get_userList, name='user_list'),
    path('login/', views.user_login, name='login'),
    path('login/successful_login/', views.user_loggedin, name='successful_login'),
    path('tasks/', views.TaskViewSet.as_view({'get': 'list', 'post':'create'}), name='tasks'),
    path('user_Login/', views.LoginViewSet.as_view({'post': 'list'}), name='user_login'),
    path('login_success/', views.SuccessViewSet.as_view({'post': 'list'}), name='successful_Login'),
    path('logout_success/', views.LogoutViewSet.as_view({'post': 'list'}), name='Logout'),
    path('logout/', views.logout, name='u_logout'),

]
