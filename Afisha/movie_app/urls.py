
from django.urls import path
from .views import *

urlpatterns = [
    path('directors/', DirectorListCreateAPIView.as_view()),
    path('directors/<int:id>/', DirectorDetailAPIView.as_view()),

    path('movies/', MovieListAPIView.as_view()),
    path('movies/<int:id>/', MovieDetailAPIView.as_view()),
    path('movies/reviews/', MovieWithReviewsAPIView.as_view()),

    path('reviews/', ReviewListAPIView.as_view()),
    path('reviews/<int:id>/', ReviewDetailAPIView.as_view()),

    path('users/register/', RegisterUserAPIView.as_view()),
    path('users/confirm/', ConfirmUserAPIView.as_view()),
]
