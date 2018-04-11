from django.db import models
import datetime

# Create your models here.

class Publisher(models.Model):
	pub_name=models.CharField(max_length=50)
	pub_addr=models.TextField(max_length=100)
	def __str__(self):
		return self.pub_name

class Category(models.Model):
	category_name=models.CharField(max_length=50)
	def __str__(self):
		return self.category_name

class Book (models.Model):
	title=models.CharField(max_length=50)
	author=models.CharField(max_length=50)
	price=models.FloatField(default=100)
	publisher=models.ForeignKey(Publisher, on_delete=models.CASCADE)
	book_category=models.ManyToManyField(Category)
	origin_date=models.DateField(auto_now_add=True)
	last_issued=models.DateField(auto_now=True)
	INSIDE='IN'
	OUTSIDE='OUT'
	STATUS_CHOICES = (
		(INSIDE,'Inside'),
		(OUTSIDE,'Outside'),
	)
	current_status=models.CharField(max_length=3, choices=STATUS_CHOICES ,default=INSIDE)
	def __str__(self):
		return self.title

class Magazine(models.Model):
	title=models.CharField(max_length=50)
	magazine_category =models.ManyToManyField(Category)
	relevance_date=models.DateField(auto_now_add=True)#datetime.datetime.now + datetime.timedelta(month=1))
	def __str__(self):
		return self.title

class Newspaper(models.Model):
	title = models.CharField(max_length=50)
	date=models.DateField(auto_now=True)
	news_category=models.ManyToManyField(Category)
	def __str__(self):
		return self.title

class Receipent(models.Model):
	receipent_name=models.CharField(max_length=100)
	receipent_advance=models.FloatField(default=0)
	STUDENT='STDNT'
	STAFF='STAFF'
	REGISTRANT_TYPE_CHOICES = (
		(STUDENT,'Student'),
		(STAFF,'Staff'),
	)
	registrant_type=models.CharField(max_length=9, choices=REGISTRANT_TYPE_CHOICES ,default=STUDENT)
	email_id=models.EmailField(max_length=50)
	join_date=models.DateField(auto_now_add=True)
	def __str__(self):
		return self.receipent_name

class Librarian(models.Model):
	librarian_name=models.TextField(max_length=100)
	email_id=models.EmailField(max_length=254)
	def __str__(self):
		return librarian_name

class Issue(models.Model):
	issue_start=models.DateField(auto_now_add=False)
	issue_end=models.DateField(auto_now=False)
	receipent=models.ForeignKey(Receipent, on_delete = models.CASCADE)
	librarian=models.ForeignKey(Librarian, on_delete = models.CASCADE)

	INSIDE='IN'
	OUTSIDE='OUT'
	STATUS_CHOICES = (
		(INSIDE,'Inside'),
		(OUTSIDE,'Outside'),
	)
	current_status=models.CharField(max_length=3, choices=STATUS_CHOICES ,default=INSIDE)
# Implement dynamic late fee
	late_fee=models.FloatField(default=0.0)
	
