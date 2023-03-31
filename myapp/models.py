from django.db import models


# Create your models here.
class Course(models.Model):
    subject = models.CharField(max_length=255)
    catalog_number = models.CharField(max_length=255)
    sub_and_cat = models.CharField(default="", max_length=255, primary_key=True)
    class_section = models.CharField(max_length=255)
    class_number = models.CharField(max_length=255)
    class_title = models.CharField(max_length=500)
    instructor = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.subject} {self.catalog_number} - {self.class_title}"


class Session(models.Model):
    tutor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    class_title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_students = models.IntegerField()


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
    
    # student model 
    
    
    # tutor model 
    class Meta:
        app_label='myapp'

    def __str__(self):
        return self.email

