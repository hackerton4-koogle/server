from django.db import models

class Language(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.name}'

class Original(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self) -> str:
        return f'{self.text}'

class Translation(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    original = models.ForeignKey(Original, on_delete=models.CASCADE)
    translated = models.TextField()

class Romanization(models.Model):
    original = models.ForeignKey(Original, on_delete=models.CASCADE)
    romanized = models.TextField()