from django.db import models
from django.contrib.auth.models import User
from admin_api.models import Category, SubCategory
from django.conf import settings

class Course(models.Model):
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='courses', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    thumbnail = models.ImageField(upload_to='course_thumbnails/')
    course_video = models.FileField(upload_to='course_videos/')
    description = models.TextField()
    what_you_will_learn = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Purchase(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student} purchased {self.course}"
