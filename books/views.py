from .utils import *
from rest_framework.views import APIView
from .serializers import *


# Create your views here.

class SearchView(APIView):
    """ An API implementation for retrieval of books meeting zero or more filter criteria from
    Project Gutenberg. Multiple filters for searching criteria are accepted as comma separated values in
    query parameters
    e.g. http://127.0.0.1:8000/books/search?book_id=14,65,54,17&language=en,fr&title=inaugural"""
    pagination_class = CustomPageNumberPagination

    def get(self, request):
        fields = ('title', 'author_info', 'genre', 'language', 'subjects', 'book_shelves', 'links')
        paginator = self.pagination_class()
        book_set1 = book_set2 = book_set3 = book_set4 = book_set5 = book_set6 = []
        book_ids = request.query_params.get('book_id')
        languages = request.query_params.get('language')
        mime_types = request.query_params.get('mime-type')
        topics = request.query_params.get('topic')
        authors = request.query_params.get('author')
        titles = request.query_params.get('title')

        if book_ids is not None:
            book_id_list = book_ids.split(',')
            book_id_list = [int(book) for book in book_id_list]
            book_set1 = fetch_books_based_on_ids(book_id_list)

        if languages is not None:
            language_list = languages.split(',')
            book_set2 = fetch_books_based_on_languages(language_list)

        if mime_types is not None:
            mime_type_list = mime_types.split(',')
            book_set3 = fetch_books_based_on_mime_type(mime_type_list)

        if topics is not None:
            topic_list = topics.split(',')
            book_set4 = fetch_books_based_on_topics(topic_list)

        if authors is not None:
            author_list = authors.split(',')
            book_set5 = fetch_books_based_on_authors(author_list)

        if titles is not None:
            title_list = titles.split(',')
            book_set6 = fetch_books_based_on_titles(title_list)

        result_set = book_set1 + book_set2 + book_set3 + book_set4 + book_set5 + book_set6

        qs = Book.objects.filter(id__in=result_set).order_by('-download_count')
        page = paginator.paginate_queryset(qs, request)
        serializer = BookSerializer(page, many=True, fields=fields)
        return paginator.get_paginated_response(serializer.data)
