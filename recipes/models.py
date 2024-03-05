from django.db import models
from django.shortcuts import reverse

# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=120)
    cooking_time = models.TextField()
    ingredients_list = models.TextField()
    difficulty = models.TextField()
    date_created = models.DateField()
    pic = models.ImageField(upload_to='recipes', default='no_picture.jpg')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse ("recipes:detail", kwargs={"pk": self.pk})
    
    def return_ingredients_as_list(self):
        return self.ingredients_list.split(",")
    
    def calculate_difficulty(self):
        num_ingredients = len(self.return_ingredients_as_list())
        if int(self.cooking_time) < 10 and int(num_ingredients) < 4:
            return "Easy"
        elif int(self.cooking_time) < 10 and int(num_ingredients) >= 4:
            return "Medium"
        elif int(self.cooking_time) >= 10 and int(num_ingredients) < 4:
            return "Intermediate"
        elif int(self.cooking_time) >= 10 and int(num_ingredients) >= 4:
            return "Hard"
        
    def save(self, *args, **kwargs):
        self.difficulty = self.calculate_difficulty()
        super().save(*args, **kwargs)