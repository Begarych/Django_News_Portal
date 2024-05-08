from django_filters import FilterSet, ModelChoiceFilter, DateTimeFilter
from .models import Post, Category
from django.forms import DateTimeInput


class PostFilter(FilterSet):
    categories = ModelChoiceFilter(queryset=Category.objects.all())
    added_after = DateTimeFilter(
        field_name='post_date',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            # 'post_date': ['lt'],
            'post_date': ['icontains'],

        }
