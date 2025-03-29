from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import Director, Movie, Review, ConfirmationCode



# DIRECTORS

class DirectorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

class DirectorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    lookup_field = 'id'

# MOVIES

class MovieListAPIView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieDetailAPIView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'id'

class MovieWithReviewsAPIView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieReviewSerializer

# REVIEWS

class ReviewListAPIView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetailAPIView(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'

# AUTH

class RegisterUserAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered. Check code.'}, status=201)
        return Response(serializer.errors, status=400)

class ConfirmUserAPIView(APIView):
    def post(self, request):
        serializer = UserConfirmSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message': 'User confirmed!'}, status=200)
        return Response(serializer.errors, status=400)
