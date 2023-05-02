from django.db import models


# Create your models here.
class Course(models.Model):
    subject = models.CharField(max_length=255)
    catalog_number = models.CharField(max_length=255)
    sub_and_cat = models.CharField(
        default="", max_length=255, primary_key=True)
    class_section = models.CharField(max_length=255)
    class_number = models.CharField(max_length=255)
    class_title = models.CharField(max_length=500)
    instructor = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.subject} {self.catalog_number} - {self.class_title}"


class Session(models.Model):
    tutor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=1)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_students = models.IntegerField()

    def __str__(self):
        return f"{self.start_time}-{self.end_time}\n{self.course}"


class AppUser(models.Model):
    email = models.CharField(max_length=320, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_student = models.BooleanField(default=False, null=True)
    is_student_true = models.BooleanField(default=False, null=True)
    STUDENT = 'STUDENT'
    TUTOR = 'TUTOR'
    USER_ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (TUTOR, 'Tutor')
    ]
    user_role = models.CharField(
        max_length=8,
        choices=USER_ROLE_CHOICES,
        default=STUDENT
    )

    class Meta:
        app_label = 'myapp'

    def __str__(self):
        return self.first_name + " " + self.last_name


class Booking(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact = models.CharField(max_length=100)
    payment = models.CharField(max_length=50)
    ACCEPTED = 'ACCEPTED'
    PENDING = 'PENDING'
    DECLINED = 'DECLINED'
    BOOKING_STATUS_CHOICES = [
        (ACCEPTED, 'Accepted'),
        (PENDING, 'Pending'),
        (DECLINED, 'Declined')
    ]
    booking_status = models.CharField(
        max_length=8,
        choices=BOOKING_STATUS_CHOICES,
        default=PENDING
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.session}"

class Profile(models.Model):
    appUser= models.ForeignKey(AppUser, on_delete= models.CASCADE)
    user= models.ForeignKey('auth.User', on_delete= models.CASCADE, primary_key=True)
    about_me = models.TextField()
    qualified_courses = models.ManyToManyField(Course, blank=True)
    image = models.ImageField(upload_to='profile_images', null=True, blank=True)

    def __str__(self):
        return f"{self.appUser} {self.user} {self.about_me}"
