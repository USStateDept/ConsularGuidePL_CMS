from django.db import models
from page.models import Page
from django.utils import timezone

# Create your models here.


class Feedback(models.Model):
	from_page = models.ForeignKey(Page, blank=True, null=True)
	text = models.TextField()
	email = models.EmailField(blank=True)
	date = models.DateTimeField(default=timezone.now)
	active = models.BooleanField(default=True, editable=False)
