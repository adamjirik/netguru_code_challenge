from django.test import TestCase
from django.db import transaction

import random
from .models import *
from .utils import *
from datetime import date
import requests
import os

# helper functions

def make_movie_objects(years=['1999']):
        movie = Movie.objects.create(title="test movie", 
                                            year=random.choice(years), 
                                            rated="PG-13", 
                                            released=date(year=1999, month=7, day=10),
                                            runtime=196,
                                            director="John Doe", 
                                            writer="John Doe",
                                            actors="John Doe, Jim Doe",
                                            language="English",
                                            country="USA")
        movie2 = Movie.objects.create(title="test movie2", 
                                            year=random.choice(years), 
                                            rated="PG-13", 
                                            released=date(year=1999, month=7, day=10),
                                            runtime=196,
                                            director="John Doe", 
                                            writer="John Doe",
                                            actors="John Doe, Jim Doe",
                                            language="English",
                                            country="USA")
        return [movie, movie2]

# Create your tests here.
class TestOmdbApi(TestCase):
    def test_can_make_call_to_omdb_api(self):
        json = make_request_to_omdb("dr+strangelove")
        self.assertIsNotNone(json)
        self.assertEqual(json["Response"], "True")

    def test_can_make_call_with_special_characters(self):
        json = make_request_to_omdb("dr strangelove")
        json2 = make_request_to_omdb("wayne's world")
        self.assertIsNotNone(json)
        self.assertEqual(json["Response"], "True")
        self.assertIsNotNone(json2)
        self.assertEqual(json2["Response"], "True")

    def test_response_keys_are_equal_to_fields(self):
        json = make_request_to_omdb("dr+strangelove")
        new_movie = format_omdb_response(json)
        for key in new_movie.keys():
            if key == 'ratings': # key shows up as ratings
                continue
            self.assertIn(key, Movie.__dict__.keys())
        for rating in new_movie['ratings']:
            for key in rating.keys():
                self.assertIn(key, Rating.__dict__.keys())

    def test_can_save_models_from_response(self):
        json = make_request_to_omdb("dr+strangelove")
        movie = format_omdb_response(json)
        new_movie = format_movie_fields(movie)
        ratings = new_movie.pop('ratings')
        movie_obj = Movie(**new_movie)
        movie_obj.save()
        for rating in ratings:
            rating_obj = Rating(**rating)
            rating_obj.movie = movie_obj
            rating_obj.save()
        saved_movies = Movie.objects.all()
        saved_ratings = Rating.objects.all()
        self.assertEqual(saved_movies.count(), 1)
        self.assertEqual(saved_ratings.count(), len(ratings))
        for rating in saved_ratings:
            self.assertIn(rating, saved_movies[0].ratings.all())

class TestMovieModel(TestCase):

    def test_can_save_object(self):
        for movie in make_movie_objects():
            movie.save()
        saved_movies = Movie.objects.all()
        self.assertEqual(saved_movies.count(), 2)

    def test_can_save_comment_to_movie(self):
        movies = make_movie_objects()
        for movie in movies:
            movie.save()
        comment = Comment.objects.create(value="Wow great movie!", movie=movies[0])
        comment.save()
        saved_movies = Movie.objects.all()
        self.assertEqual(saved_movies.count(), 2)
        saved_comments = Comment.objects.all()
        self.assertEqual(saved_comments.count(), 1)
        self.assertIn(comment, movies[0].comments.all())
        
class TestMovieViewSet(TestCase):
    def setUp(self):
        for movie in make_movie_objects():
            movie.save()

    def test_movie_post(self):
        response = self.client.post('/movies/', data={'title': "wayne's world"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Movie.objects.count(), 3)
        new_movie = Movie.objects.last()
        self.assertEqual(new_movie.title, "Wayne's World", f"Actual title was {new_movie.title}")

    def test_movie_get_list(self):
        response = self.client.get('/movies/')
        json = response.json()
        self.assertEqual(len(json), 2)
        self.assertTrue(isinstance(json[0]['ratings'], list))

    def test_movie_get_detail(self):
        movie = Movie.objects.last()
        response = self.client.get(f'/movies/{movie.id}/')
        json = response.json()
        self.assertEqual(json['title'], movie.title)


class TestCommentModel(TestCase):
    def setUp(self):
        for movie in make_movie_objects():
            movie.save()
    
    def test_can_save_object(self):
        comment = Comment.objects.create(movie=Movie.objects.first(), value="Wow great movie!")
        comment.save()
        self.assertEqual(Comment.objects.count(), 1)

    def test_comment_requries_movie(self):
        comment = Comment(value="No movie!")
        with self.assertRaises(Exception) as cm:
            with transaction.atomic():
                comment.save()
        self.assertEqual(Comment.objects.count(), 0)

    
class TestCommentViewSet(TestCase):
    def setUp(self):
        for movie in make_movie_objects():
            comment = Comment(value='comment1', movie=movie)
            comment2 = Comment(value='comment2', movie=movie)
            movie.save()
            comment.save()
            comment2.save()
    
    def test_get_all_comments(self):
        self.assertEqual(Movie.objects.count(), 2)
        self.assertEqual(Comment.objects.count(), 4)
        response = self.client.get('/comments/')
        json = response.json()
        movie_id = Movie.objects.first().id
        self.assertEqual(len(json), 4)
        self.assertIn(movie_id, [comment['movie'] for comment in json])

    def test_get_comment_by_movie_id(self):
        self.assertEqual(Movie.objects.count(), 2)
        self.assertEqual(Comment.objects.count(), 4)
        movie = Movie.objects.last()
        response = self.client.get(f'/comments/?movie={movie.id}')
        json = response.json()
        self.assertEqual(json[0]['movie'], movie.id)
        for comment in json:
            self.assertEqual(movie.id, comment['movie'])

    def test_post_comment_to_movie(self):
        movie = Movie.objects.last()
        response = self.client.post(f'/comments/', data={'value': 'wow great movie', 'movie': movie.id})
        json = response.json()
        comment = Comment.objects.get(id=json['id'])
        self.assertEqual(movie.id, json['movie'])
        movie = Movie.objects.last()
        self.assertIn(comment, movie.comments.all())





class TestTopView(TestCase):
    def setUp(self):
        movies_80s = make_movie_objects(['1980', '1981', '1982'])
        movies_90s = make_movie_objects(['1990', '1991', '1992'])
        for movie in movies_90s:
            comment = Comment(value='comment1', movie=movie)
            comment2 = Comment(value='comment2', movie=movie)
            movie.save()
            comment.save()
            comment2.save()
        for movie in movies_80s:
            comment = Comment(value='comment1', movie=movie)
            movie.save()
            comment.save()

    def test_setup(self):
        self.assertEqual(Movie.objects.count(), 4)
        self.assertEqual(Comment.objects.count(), 6)
        
    def test_can_get_top_movies_ordered_by_comment_number(self):
        response = self.client.get('/top/')
        json = response.json()
        self.assertTrue(json[0]["rank"] < json[3]["rank"])
        self.assertTrue(json[0]["comments"] > json[3]["comments"])
        self.assertTrue(json[0]["rank"] == json[1]["rank"])

    def test_can_get_top_movies_in_date_range(self):
        response = self.client.get('/top/?start=1990&end=1999')
        json = response.json()
        movies_90s = Movie.objects.filter(year__gte='1990')
        json_ids = [ranking['id'] for ranking in json]
        for id in json_ids:
            self.assertIn(id, [movie.id for movie in movies_90s])
