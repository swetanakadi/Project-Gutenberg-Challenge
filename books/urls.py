from django.urls import path
from .views import *


urlpatterns = [
    path('search', SearchView.as_view()),
    path('allBooks', AllBookView.as_view()),
    path('allAuthors', AllAuthorView.as_view()),
    path('allLanguages', AllLanguageView.as_view()),
    path('allSubjects', AllSubjectView.as_view()),
    path('allFormats', AllFormatView.as_view()),
    path('allShelves', AllShelfView.as_view()),

]
