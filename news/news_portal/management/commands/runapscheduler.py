import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.utils.timezone import now, timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from news_portal.models import Post, Subscription

logger = logging.getLogger(__name__)


def my_job():
    # Your job processing logic here...
    # last_week = now() - timedelta(days=7)
    # posts = Post.objects.filter(post_date__gte=last_week)
    # categories = set(posts.values_list('categories__id', flat=True))
    #
    # for category_id in categories:
    #     category_posts = posts.filter(categories__id=category_id)
    #     subscribers = Subscription.objects.filter(category_id=category_id).values_list('user__email', flat=True)
    #
    #     if subscribers:
    #         subject = f"Weekly Newsletter for {category_posts.first().categories.get(id=category_id).category_name}"
    #         html_message = render_to_string('weekly_newsletter.html', {'posts': category_posts})
    #         plain_message = strip_tags(html_message)
    #         from_email = 'from@example.com'
    #
    #         send_mail(subject, plain_message, from_email, subscribers, html_message=html_message)
    last_week = now() - timedelta(days=7)
    posts = Post.objects.filter(post_date__gte=last_week)
    categories = set(posts.values_list('categories__id', flat=True))

    for category_id in categories:
        category_posts = posts.filter(categories__id=category_id)
        subscribers = Subscription.objects.filter(category_id=category_id).values_list('user__email', flat=True)

        if subscribers:
            subject = f"Weekly Newsletter for {category_posts.first().categories.get(id=category_id).category_name}"
            html_message = render_to_string('weekly_newsletter.html', {'posts': category_posts})
            plain_message = strip_tags(html_message)
            from_email = 'example@gmail.com'

            for email in subscribers:
                msg = EmailMultiAlternatives(subject, plain_message, from_email, [email])
                msg.attach_alternative(html_message, "text/html")
                msg.send()


# The `close_old_connections` decorator ensures that database connections,
# that have become unusable or are obsolete, are closed before and after your
# job has run. You should use it to wrap any jobs that you schedule that access
# the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="fri", hour="18", minute="00"),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")