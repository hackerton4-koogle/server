from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="category_name")
    def __str__(self):
        return self.name

    @classmethod
    def get_others_category(cls):
        instance, _ = cls.objects.get_or_create(name='그 외')
        return instance
    
class Food(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="food_category")
    name = models.CharField(max_length=100, verbose_name="Food_name")
    def __str__(self):
            return self.name
    
    @classmethod
    def get_others_food(cls):
        instance, _ = cls.objects.get_or_create(category=Category.get_others_category(), name='기타')
        return instance