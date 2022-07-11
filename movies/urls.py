from django.urls import path

from .views import  AllReviews, DeleteReview, MovieReviewsView, MovieView, ListMovieById

urlpatterns = [
    path('movies/', MovieView.as_view()),
    path('movies/<int:movie_id>/', ListMovieById.as_view()),
    path('movies/<int:movie_id>/reviews/', MovieReviewsView.as_view()),
    path('reviews/', AllReviews.as_view()), 
    path('reviews/<int:review_id>/', DeleteReview.as_view())
]
