from django.db import models


class Sweet(models.Model):
    title = models.CharField(max_length=255, null=False)
    calories = models.PositiveIntegerField(null=False)

    def __str__(self):
        return "{} - {}".format(self.title, self.calories)
