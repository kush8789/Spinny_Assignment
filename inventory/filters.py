import django_filters
from django.db.models import F, ExpressionWrapper, FloatField
from django_filters import FilterSet, NumberFilter

class PropertyNumberFilter(django_filters.NumberFilter):
    def filter(self, qs, value):
        if value is None:
            return qs
        expression = ExpressionWrapper(F(self.field_name), output_field=FloatField())
        if self.lookup_expr == 'lt':
            return qs.annotate(temp=expression).filter(temp__lt=value)
        elif self.lookup_expr == 'gt':
            return qs.annotate(temp=expression).filter(temp__gt=value)
        return qs

class PropertyFilterSet(FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field, filter_class, lookups in self.Meta.property_fields:
            for lookup in lookups:
                self.filters[f'{field}__{lookup}'] = filter_class(field_name=field, lookup_expr=lookup)

from .models import Box

class MyBoxFilter(PropertyFilterSet):
    class Meta:
        model = Box
        fields = {
            'length': ['lt', 'gt'],
            'breadth': ['lt', 'gt'],
            'height': ['lt', 'gt'],
        }
        property_fields = [
            ('area', PropertyNumberFilter, ['lt', 'gt']),
            ('volume', PropertyNumberFilter, ['lt', 'gt']),
        ]

class BoxFilter(MyBoxFilter):
    area__lt = django_filters.NumberFilter(method='filter_area_lt')
    area__gt = django_filters.NumberFilter(method='filter_area_gt')

    class Meta(MyBoxFilter.Meta):
        fields = {
            'length': ['lt', 'gt'],
            'breadth': ['lt', 'gt'],
            'height': ['lt', 'gt'],
            'created_at': ['lt', 'gt'],
            'creator__username': ['exact'],
        }

    def filter_area_lt(self, queryset, name, value):
        return queryset.annotate(
            area=ExpressionWrapper(F('length') * F('breadth'), output_field=FloatField())
        ).filter(area__lt=value)

    def filter_area_gt(self, queryset, name, value):
        return queryset.annotate(
            area=ExpressionWrapper(F('length') * F('breadth'), output_field=FloatField())
        ).filter(area__gt=value)

    def filter_volume_lt(self, queryset, name, value):
        return queryset.annotate(
            volume=ExpressionWrapper(F('length') * F('breadth') * F('height'), output_field=FloatField())
        ).filter(volume__lt=value)

    def filter_volume_gt(self, queryset, name, value):
        return queryset.annotate(
            volume=ExpressionWrapper(F('length') * F('breadth') * F('height'), output_field=FloatField())
        ).filter(volume__gt=value)
