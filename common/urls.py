from django.urls import path
from django.contrib.auth import views as auth_views

app_name ='common'

urlpatterns = [
    path("login/",
     auth_views.LoginView.as_view(template_name='common/login.html'),  # get과 post를 모두 처리
      name="login"),
      path('logout/', auth_views.LogoutView.as_view(), name='logout')
]
