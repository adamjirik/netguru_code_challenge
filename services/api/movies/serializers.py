from rest_framework import serializers
from django.db.models import Count
from django.forms.models import model_to_dict
from .models import *
from .utils import *
from .exceptions import MovieNotFoundException

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['source', 'value']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    ratings = RatingSerializer(many=True, allow_null=True, read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = [key for key in list(model_to_dict(Movie).keys()) if key != 'title']

    def create(self, validated_data):
        data = make_request_and_format(validated_data['title'])
        if data['response'] == 'False':
            raise MovieNotFoundException
        else:
            data.pop('response')
        ratings_data = data.pop('ratings')
        movie = Movie.objects.create(**data)
        for rating in ratings_data:
            Rating.objects.create(movie=movie, **rating)
        return movie

    def get_comments(self, obj):
        return obj.comments.count()

class TopSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = ['id', 'comments', 'rank']

    def get_comments(self, obj):

        return obj.comments.count()

    def get_rank(self, obj):
        rank = 1
        current_count = None
        last_count = None
        movies = Movie.objects.annotate(count=Count('comments__id')).order_by('count').reverse() # get all movies ordered by the number of comments decending
        for i, movie in enumerate(movies):
            if i > 0:
                last_count = movies[i-1].count
            current_count = movie.count
            if last_count is not None and current_count < last_count:
                rank += 1
            if obj.id == movie.id:
                return rank
            

            

        
