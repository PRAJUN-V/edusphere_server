from django.urls import path
from .views import instructor_chatrooms, StudentChatroomsView

urlpatterns = [
    path('instructor/chatroom/<int:instructor_id>/', instructor_chatrooms, name='instructor_chatrooms'),
    path('student/chatroom/<int:student_id>/', StudentChatroomsView.as_view(), name='student-chatrooms'),
    # path('chatroom/<int:room_id>/', ChatListView.as_view(), name='chat-list'),
]
