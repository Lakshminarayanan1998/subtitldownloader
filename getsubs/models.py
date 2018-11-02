from django.db import models


class StoreData(models.Model):
        movie_title=models.TextField(max_length=10000)
        movie_link=models.TextField(max_length=100000)
