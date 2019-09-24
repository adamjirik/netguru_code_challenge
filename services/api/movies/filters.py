from rest_framework import filters
from django.forms.models import model_to_dict
from .models import Movie

class YearRangeFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        start = request.query_params.get('start', None)
        end = request.query_params.get('end', None)
        if start is not None:
            queryset = queryset.filter(year__gte=start)
        if end is not None:
            queryset = queryset.filter(year__lte=end)
        return queryset

class MovieFieldFilterBackend(filters.BaseFilterBackend):
    
    def filter_queryset(self, request, queryset, view):
        params = request.query_params
        contains_fields = list(model_to_dict(Movie).keys())
        greater_than_fields = [contains_fields.pop(contains_fields.index(key)) for key in ['imdbrating', 'runtime']]
        for field in contains_fields:
            param = params.get(field)
            if param is not None:
                f = {f'{field}__icontains': param}
                queryset = queryset.filter(**f)
        for field in greater_than_fields:
            param = params.get(field)
            if param is not None:
                f = {f'{field}__gte': param}
                queryset = queryset.filter(**f)
        return queryset