from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from .models import *


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


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


""" custom functions to fetch books based on given search criteria"""


def fetch_books_based_on_titles(titles):
    return list(title_matching(titles).values_list('id', flat=True))


def fetch_books_based_on_ids(books):
    return list(Book.objects.filter(gutenberg_id__in=books).values_list('id', flat=True))


def fetch_books_based_on_languages(languages):
    books = BookLanguages.objects.filter(language__in=Language.objects.filter(code__in=languages)).values_list(
        'book', flat=True)
    return list(books)


def fetch_books_based_on_mime_type(mime_types):
    books = Format.objects.filter(mime_type__in=mime_types).values_list('book', flat=True)
    return list(books)


def fetch_books_based_on_authors(authors):
    books = BookAuthors.objects.filter(author__in=authors_matching(authors)).values_list('book', flat=True)
    return list(books)


def fetch_books_based_on_topics(topics):
    subjects = list(
        BookSubjects.objects.filter(subject__in=subjects_matching(topics)).values_list('book', flat=True))
    shelves = list(
        BookBookshelves.objects.filter(bookshelf__in=bookshelf_matching(topics)).values_list('book', flat=True))
    result = subjects + shelves
    return result
