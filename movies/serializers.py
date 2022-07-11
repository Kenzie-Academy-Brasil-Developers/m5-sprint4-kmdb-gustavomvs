from operator import ge
from socket import getnameinfo
from rest_framework import serializers
from genres.serializers import GenreSerializer
from genres.models import Genre
from movies.models import Movie


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    premiere = serializers.DateTimeField('%Y-%m-%d')
    duration = serializers.CharField()
    classification = serializers.IntegerField()
    synopsis = serializers.CharField()
    genres = GenreSerializer(many=True)

    def create(self, validated_data):
        genres_data = validated_data.get('genres', [])

        genres = []

        for genr in genres_data:
            (genre, is_created) = Genre.objects.get_or_create(**genr)
            genres.append(genre)

        del validated_data['genres']
        
        movie = Movie.objects.create(**validated_data)
        movie.genres.set(genres)

        return movie

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.premiere = validated_data.get('premiere', instance.premiere)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.classification = validated_data.get('classification', instance.classification)
        instance.synopsis = validated_data.get('synopsis', instance.synopsis)

        genres_data = validated_data.get(
            'genres', instance.genres)

        if (genres_data != instance.genres):
            genres = []
            for genre in genres_data:
                (genre, is_created) = Genre.objects.get_or_create(**genre)
                genres.append(genre)
            instance.genres.set(genres)

        instance.save()

        return instance
