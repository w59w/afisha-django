from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Director, Movie, Review, ConfirmationCode

class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.IntegerField(source='movie_set.count', read_only=True)

    class Meta:
        model = Director
        fields = ['id', 'name', 'movies_count']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty.")
        return value

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'duration', 'director']

    def validate_duration(self, value):
        if value <= 0:
            raise serializers.ValidationError("Duration must be positive.")
        return value

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'movie']

    def validate_stars(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Stars must be 1–5.")
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
            return round(sum(r.stars for r in reviews) / reviews.count(), 1)
        return None

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False
        )
        import random
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        ConfirmationCode.objects.create(user=user, code=code)
        print(f"Confirmation code for {user.username}: {code}")
        return user

class UserConfirmSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
            conf = ConfirmationCode.objects.get(user=user)
        except:
            raise serializers.ValidationError("Invalid username or code")
        if conf.code != data['code']:
            raise serializers.ValidationError("Wrong code")
        user.is_active = True
        user.save()
        conf.delete()
        return data
