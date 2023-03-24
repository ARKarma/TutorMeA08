from django.db import models


# Create your models here.
class Course(models.Model):
    subject = models.CharField(max_length=255)
    catalog_number = models.CharField(max_length=255)
    sub_and_cat = models.CharField(default="", max_length=255)
    class_section = models.CharField(max_length=255)
    class_number = models.CharField(max_length=255)
    class_title = models.CharField(max_length=500)
    instructor = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.subject} {self.catalog_number} - {self.class_title}"


class Session(models.Model):
    tutor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_students = models.IntegerField()
