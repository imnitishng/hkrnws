import pytz
from datetime import datetime
from .models import Post
from rest_framework import serializers

from .utils import convert_to_ist


class PostsResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "title": instance.title ,
            "story_url": instance.story_url,
            "timestamp_UTC": instance.timestamp.strftime('%d-%m-%Y %H:%M'),
            "timestamp_local": convert_to_ist(instance.timestamp),
            "post_age": str(datetime.now(pytz.timezone('UTC')) - instance.timestamp),
            "points": instance.points ,
            "comments": instance.comments ,
            "posted_by": instance.posted_by ,
            "poster_profile_url": instance.poster_profile_url ,
            "hn_post_url": instance.hn_post_url,
            "read": True if instance.id in self.context['read_ids'] else False,
            "deleted": True if instance.id in self.context['deleted_ids'] else False
        }

class PostActionRequest(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validate_id(self, value):
        try:
            post = Post.objects.get(pk=value)
        except:
            raise serializers.ValidationError("Post with the given ID is not found", code=404)
        return value

    def validate_action(self, value):
        if value not in ['read', 'hide']:
            raise serializers.ValidationError("Invalid Action. Please use 'read' or 'hide'")
        return value
