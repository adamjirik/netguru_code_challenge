from rest_framework.exceptions import APIException

class MovieNotFoundException(APIException):
    status_code = 404
    default_detail = 'Movie not found.'
    default_code = 'not_found'