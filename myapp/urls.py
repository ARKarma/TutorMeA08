
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from myapp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path("", views.home, name='home'),
    path('student-home/', views.student_home, name='student-home'),
    path('tutor-home/', views.tutor_home, name='tutor-home'),
    path('classes/', views.course_list, name='course_list'),
    path('post-session/', views.post_session, name='post-session'),
    path('course/<str:pk>/', views.view_sessions, name='sessions'),
    path('book-session/<int:session_id>/',
         views.book_session, name='book-session'),
    path('booking-confirmation/<str:course_id>/',
         views.booking_confirmation, name='booking_confirmation'),
    path('current-appointments/', views.current_appointments,
         name='current-appointments'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('profile/', views.profile, name='profile'),
    path('tutor/<int:pk>/', views.tutor_profile, name='tutor'),
    path('chat/<int:receiver_id>/', views.chat, name='chat'),
    path('start-chat/<int:user_id>/', views.start_chat, name='start-chat'),
    path('tutor-chats/', views.tutor_chats, name='tutor_chats'),
    path('student-chats/', views.student_chats, name='student_chats'),

]
