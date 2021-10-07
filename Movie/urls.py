from django.urls import path
from .views import *

urlpatterns = [
    path('movie/', MovieListView.as_view()),
    path('movie/<int:pk>', MovieDetail.as_view()),
    path('review/', ReviewCreateView.as_view()),
    path('create/movie/', CreateMovieView.as_view())

]