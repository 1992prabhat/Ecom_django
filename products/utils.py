from django.utils.text import slugify

def generate_unique_slug(model, value, instance=None):
		"""
		Generate a unique slug for a given instance based on the provided name.
		If the generated slug already exists, append a number to make it unique.

		Args:
				model: The model class for which the slug is being generated.
				value (str): The value to be used for generating the slug.
				instance: The model instance for which the slug is being generated (optional).
		"""

		base_slug = slugify(value)
		slug = base_slug
		counter = 1

		queryset = model.objects.all()
		if instance and instance.pk:
				queryset = queryset.exclude(pk=instance.pk)

		while queryset.filter(slug=slug).exists():
				slug = f"{base_slug}-{counter}"
				counter += 1

		return slug