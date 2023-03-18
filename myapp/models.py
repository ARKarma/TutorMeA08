from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email= models.CharField(max_length=320)
    STUDENT= 'STUDENT'
    TUTOR= 'TUTOR'
    USER_TYPE_CHOICES = [
        (STUDENT, 'Student'),
        (TUTOR, 'Tutor')
    ]
    user_type= models.CharField(
        max_length=8,
        choices=USER_TYPE_CHOICES,
        default=STUDENT
    )

