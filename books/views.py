from .utils import authors_matching, subjects_matching, bookshelf_matching, title_matching, \
    CustomPageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status

# Create your views here.

class SearchView(APIView):
    pagination_class = CustomPageNumberPagination

    def fetch_books_based_on_titles(self, titles):
        return list(title_matching(titles).values_list('id', flat=True))

    def fetch_books_based_on_ids(self, books):
        return list(Book.objects.filter(gutenberg_id__in=books).values_list('id', flat=True))

    def fetch_books_based_on_languages(self, languages):
        books = BookLanguages.objects.filter(language__in=Language.objects.filter(code__in=languages)).values_list(
            'book', flat=True)
        return list(books)

    def fetch_books_based_on_mime_type(self, mime_types):
        books = Format.objects.filter(mime_type__in=mime_types).values_list('book', flat=True)
        return list(books)

    def fetch_books_based_on_authors(self, authors):
        books = BookAuthors.objects.filter(author__in=authors_matching(authors)).values_list('book', flat=True)
        return list(books)

    def fetch_books_based_on_topics(self, topics):
        subjects = list(
            BookSubjects.objects.filter(subject__in=subjects_matching(topics)).values_list('book', flat=True))
        shelves = list(
            BookBookshelves.objects.filter(bookshelf__in=bookshelf_matching(topics)).values_list('book', flat=True))
        result = subjects + shelves
        return result

    def get(self, request):
        fields = ('title', 'author_info', 'genre', 'language', 'subjects', 'book_shelves', 'links')
        paginator = self.pagination_class
        print('paginator', paginator)
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
            book_set1 = self.fetch_books_based_on_ids(book_id_list)

        if languages is not None:
            language_list = languages.split(',')
            book_set2 = self.fetch_books_based_on_languages(language_list)

        if mime_types is not None:
            mime_type_list = mime_types.split(',')
            book_set3 = self.fetch_books_based_on_mime_type(mime_type_list)

        if topics is not None:
            topic_list = topics.split(',')
            book_set4 = self.fetch_books_based_on_topics(topic_list)

        if authors is not None:
            author_list = authors.split(',')
            book_set5 = self.fetch_books_based_on_authors(author_list)

        if titles is not None:
            title_list = titles.split(',')
            book_set6 = self.fetch_books_based_on_titles(title_list)

        result_set = book_set1 + book_set2 + book_set3 + book_set4 + book_set5 + book_set6

        qs = Book.objects.filter(id__in=result_set).order_by('-download_count')
        page = paginator.paginate_queryset(qs, request)
        serializer = BookSerializer(page, many=True, fields=fields)
        return paginator.get_paginated_response(serializer.data)


# class AllBookView(APIView):
#     serializer_class = BookSerializer
#
#     def get(self, request, *args, **kwargs):
#         qs = title_matching(['inaugural'])
#         print(qs.count())
#         serializer = BookSerializer(qs, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# class AllAuthorView(APIView):
#     serializer_class = AuthorSerializer
#
#     def get(self, request, *args, **kwargs):
#         qs = authors_matching(['lewis', 'mark'])
#         serializer = AuthorSerializer(qs, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# class AllLanguageView(APIView):
#     serializer_class = LanguageSerializer
#
#     def get(self, request, *args, **kwargs):
#         qs = Language.objects.all()[:10]
#         serializer = LanguageSerializer(qs, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# class AllSubjectView(APIView):
#     serializer_class = SubjectSerializer
#
#     def get(self, request, *args, **kwargs):
#         qs = Subject.objects.all()[:10]
#         serializer = SubjectSerializer(qs, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# class AllFormatView(APIView):
#     serializer_class = FormatSerializer
#
#     def get(self, request, *args, **kwargs):
#         qs = Format.objects.all()[:10]
#         serializer = FormatSerializer(qs, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# class AllShelfView(APIView):
#     serializer_class = BookShelfSerializer
#
#     def get(self, request, *args, **kwargs):
#         qs = Bookshelf.objects.all()[:10]
#         serializer = BookShelfSerializer(qs, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
