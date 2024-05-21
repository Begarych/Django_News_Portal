from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Subscription
from .filters import PostFilter
from .forms import PostForm, NewsForm
from django.urls import reverse_lazy
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect


class PostList(ListView):
    model = Post
    ordering = 'post_date'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 2


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class SearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class SearchDetail(DetailView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'


class CreatePost(PermissionRequiredMixin, CreateView):
    permission_required = ('news_portal.add_post')
    form_class = PostForm
    model = Post
    template_name = 'edit_post.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.is_post_type_news = False
        return super().form_valid(form)


class CreateNews(PermissionRequiredMixin, CreateView):
    permission_required = ('news_portal.add_post')
    form_class = NewsForm
    model = Post
    template_name = 'edit_news.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.is_post_type_news = True
        return super().form_valid(form)


class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news_portal.change_post')
    form_class = PostForm
    model = Post
    template_name = 'edit_post.html'


class NewsEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news_portal.change_post')
    form_class = NewsForm
    model = Post
    template_name = 'edit_news.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news_portal.delete_post')
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news_portal.delete_post')
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('category_name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )
