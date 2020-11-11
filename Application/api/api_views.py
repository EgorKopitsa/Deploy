from rest_framework.generics import ListAPIView, RetrieveAPIView

from .serializers import *
from ..models import Category, Top, Button, Shoes


class CategoryListAPIView(ListAPIView):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class TopListAPIView(ListAPIView):

    serializer_class = TopSerializer
    queryset = Top.objects.all()


class TopDetailAPIView(RetrieveAPIView):

    serializer_class = TopSerializer
    queryset = Top.objects.all()
    lookup_field = 'id'


class ButtonListAPIView(ListAPIView):

    serializer_class = ButtonSerializer
    queryset = Button.objects.all()


class ButtonDetailAPIView(RetrieveAPIView):

    serializer_class = ButtonSerializer
    queryset = Button.objects.all()
    lookup_field = 'id'


class ShoesListAPIView(ListAPIView):

    serializer_class = ShoesSerializer
    queryset = Shoes.objects.all()


class ShoesDetailAPIView(RetrieveAPIView):

    serializer_class = ShoesSerializer
    queryset = Shoes.objects.all()
    lookup_field = 'id'
