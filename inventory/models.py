from django.db import models
from django.contrib.auth.models import User

class Box(models.Model):
    length = models.FloatField()
    breadth = models.FloatField()
    height = models.FloatField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_boxes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    area = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only calculate if creating new instance
            self.area = self.calculate_area()
            self.volume = self.calculate_volume()
        super().save(*args, **kwargs)

    def calculate_area(self):
        return self.length * self.breadth

    def calculate_volume(self):
        return self.length * self.breadth * self.height
