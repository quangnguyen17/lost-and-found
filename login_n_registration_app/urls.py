from django.urls import path
from . import views
from login_n_registration_app.views import LoginRegistration

urlpatterns = [
    path('', LoginRegistration.as_view()),
    path('login', LoginRegistration.as_view()),
    path('register', LoginRegistration.as_view()),
]
