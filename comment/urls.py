from django.urls import path

from .views import CommentView, CommentfilterView

urlpatterns = [
        path('', CommentView.as_view()),
        path('/filter', CommentfilterView.as_view()),
]
