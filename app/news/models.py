from django.db import models
from django.urls import reverse
from django.utils import timezone
import uuid


class News(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    content = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=50, choices=(
        ('politics', 'Politics'),
        ('sports', 'Sports'),
        ('entertainment', 'Entertainment'),
        ('technology', 'Technology')
    ))
    ('created_at', models.DateTimeField(default='2023-10-21T16:00:00Z')),
    ('updated_at', models.DateTimeField(default='2023-10-21T16:00:00Z')),


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        expiration_time = timezone.now() + timezone.timedelta(hours=1)
        TemporaryLink.objects.create(news=self, token=uuid.uuid4(), expiration_time=expiration_time)


class TemporaryLink(models.Model):
    news = models.ForeignKey('News', on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    expiration_time = models.DateTimeField()

    def is_expired(self):
        return self.expiration_time < timezone.now()