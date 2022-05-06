from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image


# Create your models here.


class post(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    date_posted = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField(default=1,
                                 validators=[
                                     MaxValueValidator(10),
                                     MinValueValidator(1)
                                 ])
    review = models.TextField()
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    likes=models.ManyToManyField(User,related_name="likers",blank=True)
    dislikes=models.ManyToManyField(User,related_name="dislikers",blank=True)
    image = models.ImageField(upload_to='pictures', null=True, blank=True)

    def total_likes(self):
        return self.likes.count()
    
    def total_dislikes(self):
        return self.dislikes.count()

    def __str__(self):
        return self.title

    def save(self):
        super().save()
        if self.image:
            img = Image.open(self.image.path)
            percent = (500/float(img.size[0]))

            new_height = int((float(img.size[1])*float(percent)))
            img = img.resize((500, new_height), Image.ANTIALIAS)
            img.save(self.image.path)


class comment(models.Model):
    comment = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    post = models.ForeignKey(post, on_delete=models.CASCADE)

    def save(self):
        super().save()
