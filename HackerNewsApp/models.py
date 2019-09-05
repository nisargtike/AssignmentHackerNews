from django.db import models
from django.utils import timezone


class Article(models.Model):

    hackernews_id = models.IntegerField()
    title = models.TextField(default="NA")
    url = models.TextField()
    user = models.CharField(max_length=50)
    upvotes = models.IntegerField(default=0)
    sentiment = models.CharField(max_length=50)
    sentiment_score = models.FloatField(default=0)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return str(self.title)