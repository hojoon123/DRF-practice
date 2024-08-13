# from django.contrib.auth.models import User
# from rest_framework import viewsets
# from api2.serializers import UserSerializer, PostSerializer, CommentSerializer
# from blog.models import Post, Comment
#
#
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response

from api2.serializers import CommentSerializer, PostListSerializer, PostRetrieveSerializer, PostLikeSerializer, \
    CateTagSerializer, PostSerializerDetail
from blog.models import Post, Comment, Category, Tag


# class PostListAPIView(ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostListSerializer


# class PostRetrieveAPIView(RetrieveAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostRetrieveSerializer


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# class PostLikeAPIView(UpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostLikeSerializer
#
#     #PATCH method
#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         data = {'like': instance.like + 1}
#         serializer = self.get_serializer(instance, data=data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#
#         if getattr(instance, '_prefetched_objects_cache', None):
#             instance._prefetched_objects_cache = {}
#
#         from rest_framework.response import Response
#         return Response(serializer.data['like'])

class PostLikeAPIView(GenericAPIView):
    queryset = Post.objects.all()

    #GET method
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.like += 1
        instance.save()

        from rest_framework.response import Response
        return Response(instance.like)


class CateTagAPIView(GenericAPIView):
    def get_queryset(self):
        return Category.objects.none()
    def get(self, request, *args, **kwargs):
        cate_list = Category.objects.all()
        tag_list = Tag.objects.all()
        data = {'cateList': cate_list, 'tagList': tag_list}
        serializer = CateTagSerializer(instance=data)

        return Response(serializer.data)

class PostPageNumberPagination(PageNumberPagination):
    page_size = 3
    # page_size_query_param = 'page_size'
    # max_page_size = 100

    def get_paginated_response(self, data):
        from collections import OrderedDict
        return Response(OrderedDict([
            ('postList', data),
            ('pageCnt', self.page.paginator.num_pages),
            ('curPage', self.page.number),
        ]))

class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostPageNumberPagination

    def get_serializer_context(self):
        return {
            'request': None,
            'format': self.format_kwarg,
            'view': self
        }

def get_prev_next(instance):
    try:
        prev = instance.get_previous_by_update_dt()
    except instance.DoesNotExist:
        prev = None
    try:
        next = instance.get_next_by_update_dt()
    except instance.DoesNotExist:
        next = None

    return prev, next

class PostRetrieveAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializerDetail

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        prevInstance, nextInstance = get_prev_next(instance)
        commentList = instance.comment_set.all()
        data = {'post': instance,
                'prevPost': prevInstance,
                'nextPost': nextInstance,
                'commentList': commentList
                }
        serializer = self.get_serializer(instance=data)
        return Response(serializer.data)


    def get_serializer_context(self):
        return {
            'request': None,
            'format': self.format_kwarg,
            'view': self
        }
