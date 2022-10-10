from django.db import models
from django.utils import timezone

# Create your models here.


class Genre(models.Model):
    name = models.CharField(unique=True, max_length=50)
    publish_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['publish_date']

    def __str__(self):
        return self.name


class Novel(models.Model):
    name = models.CharField(unique=True, max_length=150)

    link = models.CharField(max_length=250)

    story = models.TextField(default='')

    img = models.ImageField(upload_to='photos/novels', default='')

    novel_type = models.CharField(max_length=150)

    date = models.CharField(max_length=150)

    author = models.CharField(max_length=150)

    lang = models.CharField(max_length=150)

    genres = models.ManyToManyField(Genre)

    publish_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return self.name


class ColNovel(models.Model):
    title = models.CharField(max_length=150)
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)

    publish_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return self.title


class Chapters(models.Model):
    title = models.CharField(max_length=150)

    col = models.ForeignKey(ColNovel, on_delete=models.CASCADE)

    content = models.TextField(default='')

    date = models.CharField(max_length=150)

    chapter = models.CharField(max_length=150)

    publish_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return f'{self.col.novel.name} - {self.col.title} - {self.chapter} - {self.title}'
