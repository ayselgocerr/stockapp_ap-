from rest_framework import serializers

from .models import Category, Blog , Comment , PostView ,Like 


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ["id"]

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"
        read_only_fields = ["id"]

    

class CommentSerializer(serializers.ModelSerializer):

    comment_count=serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["id"]


    def get_comment_count(self,comment_object):
        return comment_object.comment_set.count()

class PostViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostView
        fields = "__all__"
        read_only_fields = ["id"]

    def to_representation(self, instance):
        # Increase the view count each time the serializer is used
        instance.views += 1
        instance.save()

        # Continue with the default representation
        return super().to_representation(instance)

class LikeViewSerializer(serializers.ModelSerializer):

    like_count=serializers.SerializerMethodField()

    class Meta:
        model = Like
        fields = "__all__"
        read_only_fields = ["id"]

    def get_like_count(self,obj):
        return obj.like_set.count()

    


