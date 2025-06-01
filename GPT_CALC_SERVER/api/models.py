from django.db import models
import uuid

# Create your models here.
class Device(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	mail = models.EmailField(max_length=254)
	number_of_requests = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	deleted_at = models.DateTimeField(null=True, blank=True)
	 
	def __str__(self):
			return self.mail
	