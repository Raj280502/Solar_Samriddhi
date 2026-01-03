from django.db import models

# Create your models here.

class Residential_Info(models.Model):
    property=models.CharField(max_length=100,null=False)
    address=models.CharField(max_length=100)
    
    def __str__(self):
        return self.property
    
class RoofType(models.Model):
    rooftop=models.CharField(max_length=100,null=False)
    
    def __str__(self):
        return self.rooftop
    
class Storey(models.Model):
    stories=models.CharField(max_length=100,null=False)
    
    def __str__(self):
        return self.stories
    
class Electricity(models.Model):
    Bill=models.IntegerField(null=False)
    
    def __str__(self):
        return self.Bill
    
        
    
    
    
