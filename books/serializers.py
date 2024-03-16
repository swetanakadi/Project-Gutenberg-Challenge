from .models import *
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class BookShelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookshelf
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class BookSerializer(serializers.ModelSerializer):
    language = serializers.SerializerMethodField('get_language_code')
    author_info = serializers.SerializerMethodField('get_author_info')
    genre = serializers.SerializerMethodField('get_book_genre')
    subjects = serializers.SerializerMethodField('get_subjects')
    book_shelves = serializers.SerializerMethodField('get_book_shelves')
    links = serializers.SerializerMethodField('get_media_links')

    class Meta:
        model = Book
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_language_code(self, book):
        instance = BookLanguages.objects.filter(book=book).first()
        if instance is None:
            return
        return instance.language.code

    def get_author_info(self, book):
        fields = ('birth_year', 'death_year', 'name')
        instance = BookAuthors.objects.filter(book=book).first()
        return AuthorSerializer(instance=instance.author, fields=fields).data

    def get_book_genre(self, book):
        instance = BookBookshelves.objects.filter(book=book).first()
        if instance is None:
            return
        return instance.bookshelf.name

    def get_subjects(self, book):
        fields = ('name', )
        instances = Subject.objects.filter(
            id__in=BookSubjects.objects.filter(book=book).values_list('subject', flat=True))
        return SubjectSerializer(instances, many=True, fields=fields).data

    def get_book_shelves(self, book):
        fields = ('name', )
        instances = Bookshelf.objects.filter(
            id__in=BookBookshelves.objects.filter(book=book).values_list('bookshelf', flat=True))
        return BookShelfSerializer(instances, many=True, fields=fields).data

    def get_media_links(self, book):
        fields = ('mime_type', 'url')
        qs = Format.objects.filter(book=book)
        return FormatSerializer(qs, many=True, fields=fields).data
