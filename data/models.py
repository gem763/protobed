from django.db import models

# Create your models here.

class Newsdata(models.Model):
    text = models.TextField()
    authors = models.CharField(max_length=300, default='')
    url = models.URLField(max_length=300)
    title = models.CharField(max_length=300)
    publish_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    publisher = models.CharField(max_length=100)
    words = models.TextField()

    def __str__(self):
        return '[{publish_date} | {publisher}] {title}'.format(publish_date=self.publish_date, publisher=self.publisher, title=self.title)
