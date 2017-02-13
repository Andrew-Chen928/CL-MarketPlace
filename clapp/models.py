from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.CharField(max_length=500)
	about = models.CharField(max_length=1000)
	slogan = models.CharField(max_length=500)

	#adding phone and email
	phone = models.CharField(default='', max_length=15)
	email = models.EmailField(default='', max_length=254)
	


	def __str__(self):
		return self.user.username

class Gig(models.Model):
	GATEGORY_CHOICES = (
		("GD", "Graphics & Design"),
		("DM", "Digital & Marketing"),
		("VA", "Video & Animation"),
		("MA", "Music & Audio"),
		("PT", "Programming & Tech")
	)

	title = models.CharField(max_length=500)
	category = models.CharField(max_length=2, choices=GATEGORY_CHOICES)
	description = models.CharField(max_length=1000)
	price = models.IntegerField(default=6)
	photo = models.FileField(upload_to='media', blank=True)
	status = models.BooleanField(default=True)
	user = models.ForeignKey(User)
	create_time = models.DateTimeField(default=timezone.now)
	#add a column
	phone = models.CharField(default='', max_length=15)
	# phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	# phone_number = models.CharField(validators=[phone_regex], blank=True) # validators should be a list

	def __str__(self):
		return self.title



class Purchase(models.Model):
	gig = models.ForeignKey(Gig)
	buyer = models.ForeignKey(User)
	time = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.gig.title

class Review(models.Model):
	gig = models.ForeignKey(Gig)
	user = models.ForeignKey(User)
	content = models.CharField(max_length=500)

	def __str__(self):
		return self.content