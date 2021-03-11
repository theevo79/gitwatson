from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class News(models.Model):
	# recreate the sql database from watson.py in this class.
	newsreader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	newsurl = models.URLField(max_length=255, default="")
	language = models.CharField(max_length=3, default="")
	text_characters = models.IntegerField(default=0)
	cat1 = models.CharField(max_length=255, default="")
	cat1_score = models.FloatField(default=0.0)
	sentiment = models.CharField(max_length=255, default="")
	senti_score = models.FloatField(default=0.0)
	sadness = models.FloatField(default=0.0)
	joy = models.FloatField(default=0.0)
	fear = models.FloatField(default=0.0)
	disgust = models.FloatField(default=0.0)
	anger = models.FloatField(default=0.0)

	def __str__(self):
		return f"{self.newsurl} has {self.text_characters} characters, it is in the category {self.cat1} with {self.cat1_score} accuracy. Its sentiment is {self.sentiment} with a score of {self.senti_score}. Its sadness score is {self.sadness}, joy {self.joy}, fear {self.fear}, disgust {self.disgust} and anger {self.anger}."

class Ents(models.Model):
	newsreader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	enturl = models.URLField(max_length=255, default="")
	enttype = models.CharField(max_length=255, default="")
	enttext = models.CharField(max_length=255, default="")
	entsenti = models.CharField(max_length=255, default="")
	entsentiscore = models.FloatField(default=0.0)
	entrele = models.FloatField(default=0.0)
	entcount = models.FloatField(default=0.0)
	entcon = models.FloatField(default=0.0)

	def __str__(self):
		return f"{self.newsreader} has read {self.enturl} which is focused on the {self.enttype} {self.enttext}. It is {self.entsenti} with a score of {self.entsentiscore}. Relevance {self.entrele}, counts {self.entcount}, confidence {self.entcon}."

