from django.db import models

# Create your models here.
class User(models.Model):
    email = models.CharField(max_length=320, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    STUDENT= 'STUDENT'
    TUTOR= 'TUTOR'
    USER_ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (TUTOR, 'Tutor')
    ]
    user_role= models.CharField(
        max_length=8,
        choices=USER_ROLE_CHOICES,
        default=STUDENT
    )
    #Maybe make separate user models for student and tutor; maybe both have foreign keys to the overall userbase model?
    class Meta:
        app_label='myapp'

    def __str__(self):
        return self.email

