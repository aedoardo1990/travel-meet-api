from django.db import models
from django.contrib.auth.models import User
from tagulous.models import TagField
from cloudinary_storage.storage import VideoMediaCloudinaryStorage
from cloudinary_storage.validators import validate_video


class Post(models.Model):
    """
    Model to create posts with images, videos, tags
    and geolocalisation
    """
    image_filter_choices = [
        ('_1977', '1977'), ('brannan', 'Brannan'),
        ('earlybird', 'Earlybird'), ('hudson', 'Hudson'),
        ('inkwell', 'Inkwell'), ('lofi', 'Lo-Fi'),
        ('kelvin', 'Kelvin'), ('normal', 'Normal'),
        ('nashville', 'Nashville'), ('rise', 'Rise'),
        ('toaster', 'Toaster'), ('valencia', 'Valencia'),
        ('walden', 'Walden'), ('xpro2', 'X-pro II')
        ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/',
        default='../default_post_hdubyv',
        blank=True
    )
    video = models.FileField(
        upload_to='videos/',
        default='../default_video_t7zkzc',
        blank=True,
        storage=VideoMediaCloudinaryStorage(),
        validators=[validate_video]
    )
    image_filter = models.CharField(
        max_length=32, choices=image_filter_choices, default='normal'
    )
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    formatted_address = models.CharField(max_length=300)
    place_id = models.CharField(max_length=300)
    tags = TagField(force_lowercase=True, max_count=15)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.id} {self.title}"