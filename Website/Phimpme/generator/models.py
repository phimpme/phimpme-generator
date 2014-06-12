from django.db import models

# Create your models here.
'''
class AppConfig(models.Model):
    name = models.CharField(max_length = 20)
    logo = models.ImageField()
    # The followings should be updated with Configuration.java in Andorid app
    enable_map = models.BooleanField()
    enable_photo_capturing = models.BooleanField()
    enable_choose_from_library = models.BooleanField()
    enable_photo_manipulation = models.BooleanField()
    enable_photo_location_modification = models.BooleanField()
    enable_nfc = models.BooleanField()
    enable_sharing_to_weibo = models.BooleanField()
    enable_sharing_to_wordpress = models.BooleanField()

class Order(models.Model):
    pass
    # TODO: Add auth part
'''