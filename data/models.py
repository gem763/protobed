from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.

class Newsdata(models.Model):
    pub = models.CharField(max_length=100)
    authors = ArrayField(models.CharField(max_length=300)) #models.CharField(max_length=500, default='')
    title = models.CharField(max_length=500)
    category = models.CharField(max_length=300, default='', null=True, blank=True)
    published_at = models.DateTimeField(auto_now_add=False, auto_now=False)
    downloaded_at = models.DateTimeField(auto_now_add=False, auto_now=False)
    text = models.TextField()
    description = models.TextField()
    top_image = models.URLField(max_length=500, blank=True)
    url = models.URLField(max_length=500)
    language = models.CharField(max_length=50)
    # words = models.TextField()
    words = ArrayField(models.CharField(max_length=200))

    def __str__(self):
        return '[{published_at} | {pub}] {title}'.format(published_at=self.published_at.date(), pub=self.pub, title=self.title)
