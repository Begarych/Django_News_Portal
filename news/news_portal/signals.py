from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models.signals import m2m_changed
from django.template.loader import render_to_string
from django.dispatch import receiver
from django.utils.html import strip_tags


from .models import Subscription, Post


# def send_notify(preview, pk, title, subscribers):
#     html_content = render_to_string(
#         'post_created_email.html',
#         {
#             'text': preview,
#             'link': f'http://127.0.0.1:8000/news/{pk}'
#         }
#     )
#
#     msg = EmailMultiAlternatives(
#         subject=title,
#         body='lol',
#         from_email='bogdan.lar@gmail.com',
#         to=subscribers
#     )
#
#     msg.attach_alternative(html_content, 'text/html')
#     msg.send()
#
#
# @receiver(m2m_changed, sender=PostCategory)
# def notify_about_new_post(sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add':
#         mail = Subscription.user.
#         for category in categories:
#             subscribers += category.subscribers.all()
#
#         subscribers = [s.email for s in subscribers]
#
#         send_notify(instance.preview(), instance.pk, instance.title, subscribers)

@receiver(m2m_changed, sender=Post.categories.through)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == "post_add":
        categories = instance.categories.all()
        subscribers = set()

        for category in categories:
            subscriptions = Subscription.objects.filter(category=category)
            for subscription in subscriptions:
                subscribers.add(subscription.user.email)

        subject = f"New post in category {', '.join([cat.category_name for cat in categories])}"
        html_message = render_to_string('post_created_email.html', {'post': instance})
        plain_message = strip_tags(html_message)
        from_email = 'bogdan.lar@gmail.com'

        send_mail(subject, plain_message, from_email, list(subscribers), html_message=html_message)
