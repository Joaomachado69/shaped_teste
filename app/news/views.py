from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from news.models import News
from news.serializers import NewsSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView

# Classe de paginação personalizada
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # Defina o número de itens por página aqui.
    page_size_query_param = 'page_size'
    max_page_size = 100

class NewsAPIView(ListAPIView):  # Alteramos a classe base para ListAPIView
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    pagination_class = StandardResultsSetPagination  # Usamos a classe de paginação personalizada

    def post(self, request) -> Response:
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            news_article = News.objects.get(pk=pk)
        except News.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = NewsSerializer(news_article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            news_article = News.objects.get(pk=pk)
        except News.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        news_article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
