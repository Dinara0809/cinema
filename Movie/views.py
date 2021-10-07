from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import Response
from .models import *
from .serializers import *


class CreateMovieView(APIView):
    def post(self, request):
        movie= MovieSerializer(data=request.data)
        if movie.is_valid():
            movie.save()
        return Response(status=201)


class ReviewCreateView(APIView):
    def post(self, request):
        review=ReviewCreate(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)

class MovieListView(APIView):
    def get(self, request):
        movies = Movie.objects.filter(draft=False)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetail(APIView):
    def get(self, request, pk):
        movie=Movie.objects.get(id=pk, draft=False)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)


