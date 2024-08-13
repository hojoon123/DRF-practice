from rest_framework import serializers
from django.contrib.auth.models import User

from blog.models import Post, Comment, Category, Tag


#
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'is_staff']
#
#
# class PostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ['id','title', 'image', 'like', 'category']
#
# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = '__all__'

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class PostRetrieveSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True)
    update_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'image', 'content', 'update_dt', 'like', 'category', 'tags']

class PostListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    class Meta:
        model = Post
        fields = ['id', 'title', 'image', 'like', 'category']

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['like']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

# class CateTagSerializer(serializers.Serializer):
#     cateList = CategorySerializer(many=True)
#     tagList = TagSerializer(many=True)

class CateTagSerializer(serializers.Serializer):
    cateList = serializers.ListField(child=serializers.CharField())
    tagList = serializers.ListField(child=serializers.CharField())


class PostSerializerSub(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title']


class CommentSerializerSub(serializers.ModelSerializer):
    update_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = Comment
        fields = ['id', 'content', 'update_dt']

class PostSerializerDetail(serializers.Serializer):
    post = PostRetrieveSerializer()
    prevPost = PostSerializerSub()
    nextPost = PostSerializerSub()
    commentList = CommentSerializerSub(many=True)