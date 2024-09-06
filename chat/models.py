from courses.models import Course
from django.contrib.auth.models import User
from django.db import models

class Chatroom(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='chatroom')
    name = models.CharField(max_length=255, null=True, blank=True)
    members = models.ManyToManyField(User, related_name='chatrooms')

    def __str__(self):
        return self.course.title
    
class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='send_messages', null=True, blank=True)
    chatroom = models.ForeignKey('Chatroom', on_delete=models.CASCADE, related_name='chats')
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


    # image_url = models.URLField(max_length=255, null=True, blank=True)
    # date = models.DateTimeField(auto_now_add=True)
    # is_read_by = models.ManyToManyField(User, related_name='read_messages', blank=True)

    def __str__(self):
        return f"{self.sender} in {self.chatroom.course.title}"
