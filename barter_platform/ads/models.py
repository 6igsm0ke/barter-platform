from django.db import models

# Create your models here.
class Ad(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE) 
    title = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    condition = models.ForeignKey('Condition', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
