from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from movies.serializers import MovieSerializer
from movies.models import Movie
from movies.permissions import MoviePermission, ReviewPermission
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from reviews.serializers import ReviewSerializer
from reviews.models import Review
class MovieView(APIView):

    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated]

    def post(self, request):
     
        serializer = MovieSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, 400)

        serializer.save()
        return Response(serializer.data, 201)

    def get(self, request):
        movies = Movie.objects.all()
        serializer_response = MovieSerializer(movies, many=True)
        return Response(serializer_response.data)


class ListMovieById(APIView):

    authentication_classes = [TokenAuthentication]

    permission_classes = [MoviePermission, IsAuthenticated]

    def get(self, request, movie_id):
        try:
            movie = Movie.objects.get(id=movie_id)
            serializer_response = MovieSerializer(movie)
            return Response(serializer_response.data)
        except Movie.DoesNotExist:
            return Response({'message': 'not found.'}, 404)

    def patch(self, request, movie_id):
        try:
            movie = Movie.objects.get(id=movie_id)
            serializer = MovieSerializer(
                movie, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, 400)
            serializer.save()
            return Response(serializer.data)
        except Movie.DoesNotExist:
            return Response({'message': 'not found.'}, 404)

    def delete(self, request, movie_id):
        try:
            movie = Movie.objects.get(id=movie_id)
            movie.delete()
            return Response({'message': 'movie deleted.'})
        except Movie.DoesNotExist:
            return Response({'message': 'not found.'}, 404)


class MovieReviewsView(APIView):

    permission_classes = [ReviewPermission]

    def post(self, request, movie_id):
        
        try:
            movie = Movie.objects.get(id=movie_id)
            serializer = ReviewSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, 400)

            serializer.save(movie_id=movie, critic=request.user)

            return Response(serializer.data,201)
        except Movie.DoesNotExist:
            return Response({'message': 'movie not found.'}, 404)

    def get(self, request, movie_id):
        try:
            movie = Movie.objects.get(id=movie_id)
            reviews = Review.objects.filter(movie_id=movie)
            serializer = ReviewSerializer(reviews, many=True)

            return Response(serializer.data)
        except Movie.DoesNotExist:
            return Response({'message': 'movie not found.'}, 404)

class AllReviews(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer_response = ReviewSerializer(reviews, many=True)
        return Response(serializer_response.data)

class DeleteReview(APIView):

    permission_classes = [ReviewPermission]

    def delete(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)
            if request.user.is_superuser or review.critic.id == request.user.id:
                review.delete()
                return Response({'message': 'review deleted successfully.'})
            return Response({"message": "You not have permission"}, 403)
        except Review.DoesNotExist:
            return Response({'message': 'review not found.'}, 404)

        