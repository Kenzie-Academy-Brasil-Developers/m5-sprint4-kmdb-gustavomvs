from rest_framework import serializers
from reviews.models import Review


class CriticSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)


class ReviewSerializer(serializers.ModelSerializer):

    critic = CriticSerializer(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ["id"]
        extra_kwargs = {"movie_id": {"required": False}, "critic": {"required": False}}

    def create(self, validated_data):
        return Review.objects.create(**validated_data)
