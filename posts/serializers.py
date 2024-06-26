from rest_framework import serializers
from .models import Post
from tagulous.contrib.drf import TagSerializer


class PostSerializer (serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    def validate_image(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image size larger than 2MB!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px'
            )
        return value
    
    def validate_video(self, value):
        if value.size > 1024 * 1024 * 60:
            raise serializers.ValidationError(
                "Video size can't be larger than 60MB!"
            )
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'created_at', 'updated_at',
            'profile_id', 'profile_image', 'is_owner',
            'title', 'content', 'image', 'video',
            'latitude', 'longitude', 'formatted_address',
            'place_id', 'tags', 'image_filter',
        ]


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model."""

    class Meta:
        model = Post.tags.tag_model
        fields = ["id", "name"]