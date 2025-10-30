from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Medicine(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    analogs = models.TextField(blank=True)
    image = models.ImageField(upload_to="medicines/", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.TextField(blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to="news/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Pharmacy(models.Model):
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=50, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    working_hours = models.CharField(max_length=120, blank=True)
    image = models.ImageField(upload_to="pharmacies/", blank=True, null=True)  # ✅ yangi qo‘shildi
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name



class Inventory(models.Model):
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('pharmacy', 'medicine')

    def __str__(self):
        return f"{self.medicine.name} @ {self.pharmacy.name}"
