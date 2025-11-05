from django.db import models

class Mobiles(models.Model):
    title = models.CharField(max_length=255, blank=True)
    brand=models.CharField(max_length=100,blank=False)
    image=models.URLField()
    
    # uploaded_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     # return self.title or f"File {self.id}"
