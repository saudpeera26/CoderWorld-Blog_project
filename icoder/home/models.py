from django.db import models

# Create your models here.
class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name= models.CharField(max_length=255)
    phone= models.IntegerField()
    email=models.EmailField()
    content= models.TextField()
    timeStamp =models.DateTimeField(auto_now_add=True ,blank=True)


    def __str__(self):
        return "Mesaage From:" + self.name + ' - ' + self.email
   
