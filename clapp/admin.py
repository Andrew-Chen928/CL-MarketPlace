from django.forms import TextInput, Textarea
from django.contrib import admin
from django.db import models
from .models import Profile, Gig, Purchase, Review

# Register your models here.

class GigAdmin(admin.ModelAdmin):
	list_display = ['title', 'user', 'price', 'create_time', 'category']
	list_filter = ('user', 'create_time', 'price', 'category')

admin.site.register(Profile)
admin.site.register(Gig, GigAdmin)
admin.site.register(Purchase)
admin.site.register(Review)
