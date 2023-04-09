from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterUser.as_view()),
    path('google-details/', views.google_user_details),
    path('user-details/', views.user_details),
    path('note/create-update/', views.create_update_note),
    path('note/list/', views.NoteListView.as_view()),
    path('note/delete/<str:title>/', views.NoteDeleteView.as_view()),
    path('note/search/<str:title>/', views.search_for_note),
]
