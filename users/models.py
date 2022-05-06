from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',
                              upload_to='profile_pics', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} profile"

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        if (self.image):
            img = Image.open(self.image.path)

            percent = (300/float(img.size[1]))

            new_width = int((float(img.size[0])*float(percent)))
            img = img.resize((new_width, 300), Image.ANTIALIAS)
            img.save(self.image.path)
