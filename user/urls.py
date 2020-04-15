from django.urls import path

from .views import SigninView, SignupView, UserView

urlpatterns = [
        path('', UserView.as_view()),
        path('/signin', SigninView.as_view()),
        path('/signup', SignupView.as_view()),
]

