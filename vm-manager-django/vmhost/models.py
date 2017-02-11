from django.db import models


class Vmhost(models.Model):
	name=models.CharField(max_length=200)
	virtType=models.CharField(max_length=200)
	
class Guest(models.Model):
	vmhost=	models.ForeignKey(Vmhost)
	name=models.CharField(max_length=200)
	currCpu=models.CharField(max_length=200)
	currMemory=models.CharField(max_length=200)

# Create your models here.
