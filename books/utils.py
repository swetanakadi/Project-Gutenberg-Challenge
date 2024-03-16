from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

from .models import Author, Subject, Bookshelf, Book


def authors_matching(authors):
    """
    Return a queryset for authors whose names contain case-insensitive
    matches for any of the `name`.
    """
    q = Q()
    for author in authors:
        q |= Q(name__icontains=author)
    return Author.objects.filter(q)


def subjects_matching(subjects):
    """
    Return a queryset for subjects whose names contain case-insensitive
    matches for any of the `names`.
    """
    q = Q()
    for subject in subjects:
        q |= Q(name__icontains=subject)
    return Subject.objects.filter(q)


def bookshelf_matching(book_shelves):
    """
    Return a queryset for bookshelves whose names contain case-insensitive
    matches for any of the `name`.
    """
    q = Q()
    for book_shelf in book_shelves:
        q |= Q(name__icontains=book_shelf)
    return Bookshelf.objects.filter(q)


def title_matching(titles):
    """
        Return a queryset for books whose names contain case-insensitive
        matches for any of the `title`.
        """
    q = Q()
    for title in titles:
        q |= Q(title__icontains=title)
    return Book.objects.filter(q)


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
