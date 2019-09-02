from django.db import models

# Create your models here.

class Newsdata(models.Model):
    pub = models.CharField(max_length=100)
    authors = models.CharField(max_length=300, default='')
    title = models.CharField(max_length=300)
    category = models.CharField(max_length=300, default='')
    published_at = models.DateTimeField(auto_now_add=False, auto_now=False)
    downloaded_at = models.DateTimeField(auto_now_add=False, auto_now=False)
    text = models.TextField()
    description = models.TextField()
    top_image = models.URLField(max_length=300)
    url = models.URLField(max_length=300)
    words = models.TextField()
    language = models.CharField(max_length=50)

    def __str__(self):
        return '[{published_at} | {pub}] {title}'.format(published_at=self.published_at, pub=self.pub, title=self.title)
