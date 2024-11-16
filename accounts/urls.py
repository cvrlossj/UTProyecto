from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import CustomLoginForm
from .views import CustomLoginView, LogoutView  # Importa tu vista personalizada

app_name = "accounts"

urlpatterns = [
    path("login/", CustomLoginView.as_view(
        template_name="accounts/login.html",
        authentication_form=CustomLoginForm
    ), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]