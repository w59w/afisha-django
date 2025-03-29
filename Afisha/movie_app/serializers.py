from rest_framework import serializers
from .models import Director, Movie, Review


class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.IntegerField(source='movie_set.count', read_only=True)

    class Meta:
        model = Director
        fields = ['id', 'name', 'movies_count']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty or whitespace.")
        return value


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'duration', 'director']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_duration(self, value):
        if value <= 0:
            raise serializers.ValidationError("Duration must be a positive number.")
        return value

    def validate_director(self, value):
        if not Director.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Director with this ID does not exist.")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'movie']

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Review text cannot be empty.")
        return value

    def validate_stars(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Stars must be between 1 and 5.")
        return value

    def validate_movie(self, value):
        if not Movie.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Movie with this ID does not exist.")
        return value


class MovieReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True, source='review_set')
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'duration', 'director', 'reviews', 'rating']

    def get_rating(self, obj):
        reviews = obj.review_set.all()
        if reviews.exists():
            return round(sum([r.stars for r in reviews]) / reviews.count(), 1)
        return None
