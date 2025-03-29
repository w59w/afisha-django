from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Director, Movie, Review
from .serializers import *

@api_view(['GET', 'POST'])
def director_list(request):
    if request.method == 'GET':
        serializer = DirectorSerializer(Director.objects.all(), many=True)
        return Response(serializer.data)
    serializer = DirectorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def director_detail(request, id):
    director = get_object_or_404(Director, id=id)
    if request.method == 'GET':
        return Response(DirectorSerializer(director).data)
    elif request.method == 'PUT':
        serializer = DirectorSerializer(director, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    director.delete()
    return Response(status=204)

@api_view(['GET'])
def movie_list(request):
    serializer = MovieSerializer(Movie.objects.all(), many=True)
    return Response(serializer.data)

@api_view(['GET'])
def movie_detail(request, id):
    movie = get_object_or_404(Movie, id=id)
    return Response(MovieSerializer(movie).data)

@api_view(['GET'])
def movie_reviews(request):
    serializer = MovieReviewSerializer(Movie.objects.all(), many=True)
    return Response(serializer.data)

@api_view(['GET'])
def review_list(request):
    serializer = ReviewSerializer(Review.objects.all(), many=True)
    return Response(serializer.data)

@api_view(['GET'])
def review_detail(request, id):
    review = get_object_or_404(Review, id=id)
    return Response(ReviewSerializer(review).data)

@api_view(['POST'])
def register_user(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User registered. Check code.'}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def confirm_user(request):
    serializer = UserConfirmSerializer(data=request.data)
    if serializer.is_valid():
        return Response({'message': 'User confirmed!'}, status=200)
    return Response(serializer.errors, status=400)
