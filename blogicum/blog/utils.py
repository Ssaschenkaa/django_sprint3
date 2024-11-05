from django.utils import timezone

from .models import Post


def get_posts(**filters):
    filters_dict = {
        'is_published': True,
        'pub_date__lte': timezone.now(),
        'category__is_published': True
    }
    filters_dict.update(filters)
    return Post.objects.filter(**filters_dict)
