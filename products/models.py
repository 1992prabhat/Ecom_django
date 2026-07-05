from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from .utils import generate_unique_slug
# Create your models here.
class Product(models.Model):
		name = models.CharField(max_length=255)
		price = models.DecimalField(max_digits=10, decimal_places=2)
		stock = models.IntegerField()
		description = CKEditor5Field(config_name='basic')
		image = models.ImageField(upload_to='products/')
		slug = models.SlugField(max_length=255, unique=True, blank=True)
		active = models.BooleanField(default=True)
		created_at = models.DateTimeField(auto_now_add=True)
		updated_at = models.DateTimeField(auto_now=True)

		def __str__(self):
				return self.name

		def save(self, *args, **kwargs):
				if not self.slug:
						self.slug = generate_unique_slug(Product, self.name, instance=self)
				super().save(*args, **kwargs)
