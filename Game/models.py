from django.db import models

class Player(models.Model):
    user_id = models.CharField(max_length = 1024)
    machine = models.BinaryField(max_length = 1024 ** 2, blank = True)

    def __str__(self):
        return self.user_id
