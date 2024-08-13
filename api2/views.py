from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api2.serializers import CommentSerializer, PostListSerializer, PostRetrieveSerializer, PostLikeSerializer, \
    CateTagSerializer, PostSerializerDetail, PostSerializerSub, CommentSerializerSub
from blog.models import Post, Comment, Category, Tag


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

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

    def get_paginated_response(self, data):
        from collections import OrderedDict
        return Response(OrderedDict([
            ('postList', data),
            ('pageCnt', self.page.paginator.num_pages),
            ('curPage', self.page.number),
        ]))


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


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    retrieve_serializer_class = PostRetrieveSerializer
    pagination_class = PostPageNumberPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.retrieve_serializer_class
        return super().get_serializer_class()

    def get_serializer_context(self):
        return {
            'request': None,
            'format': self.format_kwarg,
            'view': self
        }

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        prevInstance, nextInstance = get_prev_next(instance)
        commentList = instance.comment_set.all()

        # 여기서 각각의 serializer를 사용하여 직렬화
        post_serializer = self.get_serializer(instance)
        prev_serializer = PostSerializerSub(prevInstance) if prevInstance else None
        next_serializer = PostSerializerSub(nextInstance) if nextInstance else None
        comment_serializer = CommentSerializerSub(commentList, many=True)

        data = {
            'post': post_serializer.data,
            'prevPost': prev_serializer.data if prev_serializer else None,
            'nextPost': next_serializer.data if next_serializer else None,
            'commentList': comment_serializer.data
        }
        return Response(data)

        # GET method
    def like(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.like += 1
        instance.save()

        return Response(instance.like)