from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from .utils import *

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        movie_id = self.request.query_params.get('movie', None)
        if movie_id is not None:
            queryset = queryset.filter(movie__id=movie_id)
        return queryset

    # def create(self, request):
    #     movie_id = self.request.data['movie']
    #     if movie_id is not None:
    #         try:
    #             movie = Movie.objects.get(id=movie_id)
    #         except:
    #             return Response({"response": "Movie not found!"}, status=status.HTTP_404_NOT_FOUND)
    #     comment_serializer = CommentSerializer(data=request.data)
    #     return 
        

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def create(self, request):
        title = request.data["title"]
        movie = make_request_and_format(title)
        movie_serializer = MovieSerializer(data=movie)
        movie_serializer.is_valid(raise_exception=True)
        movie_obj = movie_serializer.save()
        return Response(movie_serializer.data, status=status.HTTP_201_CREATED)

class TopViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.annotate(total_comments=Count('comments__id')).order_by('total_comments').reverse()
    serializer_class = TopSerializer
    # ordering = ['comments']

    def get_queryset(self):
        queryset = Movie.objects.annotate(total_comments=Count('comments__id')).order_by('total_comments').reverse()
        start = self.request.query_params.get('start', None)
        end = self.request.query_params.get('end', None)
        if start is not None:
            queryset = queryset.filter(year__gte=start)
        if end is not None:
            queryset = queryset.filter(year__lte=end)
        return queryset