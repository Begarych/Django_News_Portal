from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Category
import datetime


@shared_task
def send_mail_task(pk):
    post = Post.objects.get(pk=pk)
    categories = post.categories.all()
    subscribers_emails = []
    for category in categories:
        subscribers_emails += category.subscriptions.values_list('user__email', flat=True)
    subscribers_emails = set(subscribers_emails)

    html_content = render_to_string('post_created_email.html',
                                    {
                                        'text': f'{post.title}',
                                        'link': f'http://127.0.0.1:8000/news/{pk}'
                                    }
                                    )

    msg = EmailMultiAlternatives(
        subject='title',
        body='',
        from_email='bogdan.lar@gmail.com',
        to=subscribers_emails
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def weekly_send_email_task():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(post_date__gte=last_week)
    categories = set(posts.values_list('categories__category_name', flat=True))
    subscribers = set(Category.objects.filter(category_name__in=categories).values_list('subscriptions__user__email',
                                                                                        flat=True))

    html_content = render_to_string('weekly_newsletter.html',
                                    {
                                        'link': 'http://127.0.0.1:8000',
                                        'post': posts,
                                    }
                                    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email='bogdan.lar@gmail.com',
        to=subscribers
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
