from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Chatroom
from courses.models import Course, Purchase

@receiver(post_save, sender=Course)
def create_chatroom(sender, instance, created, **kwargs):
    if created:
        Chatroom.objects.create(
            course=instance,
            name=f"{instance.title}"
        )

@receiver(post_save, sender=Purchase)
def add_student_to_chatroom(sender, instance, created, **kwargs):
    if created:
        chatroom, created = Chatroom.objects.get_or_create(course=instance.course)
        chatroom.members.add(instance.student)
