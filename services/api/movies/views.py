from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from .utils import *
from .filters import *
from rest_framework import filters


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class CommentViewSet(viewsets.ModelViewSet):

    '''
    List all comments or comments by movie_id
    parameters:
    movie - the movie id
    '''

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        movie_id = self.request.query_params.get('movie', None)
        if movie_id is not None:
            queryset = queryset.filter(movie__id=movie_id)
        return queryset
        

class MovieViewSet(viewsets.ModelViewSet):
    '''
    List all movies
    '''
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [YearRangeFilterBackend, MovieFieldFilterBackend, filters.OrderingFilter]

    def create(self, request):
        movie_serializer = MovieSerializer(data=request.data)
        movie_serializer.is_valid(raise_exception=True)
        movie_obj = movie_serializer.save()
        return Response(movie_serializer.data, status=status.HTTP_201_CREATED)
        

class TopViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    List movies in order by number of comments
    parameters:
    start - the beginning year in the range of movies to list
    end - the end year in the range of movies to list
    '''
    queryset = Movie.objects.annotate(total_comments=Count('comments__id')).order_by('total_comments').reverse()
    serializer_class = TopSerializer
    filter_backends = [YearRangeFilterBackend]