from django.shortcuts import get_object_or_404, render

from blog.models import Category

from .utils import get_posts


NUMBER_OF_POSTS = 5


def index(request):
    template = 'blog/index.html'
    posts = get_posts()[:NUMBER_OF_POSTS]
    context = {'post_list': posts}
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'
    post = get_object_or_404(get_posts(),
                             pk=post_id)
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_slug
    )
    post = get_posts(category=category)
    context = {'category': category, 'post_list': post}
    return render(request, template, context)
