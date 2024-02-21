from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ..models import Genre

class GenreView(ViewSet):

    def retrieve(self, request, pk):
        """Handle GET requests for a single tag
          
        returns:
        Response -- JSON Serialzied tag"""
        try:
            genre = Genre.objects.get(pk=pk)
            serializer = GenreSerializer(genre)
            return Response(serializer.data)
        except Genre.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests for every Order

        Returns:
            Response -- JSON serialized Orders
        """
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)


class GenreSerializer(serializers.ModelSerializer):
    """JSON serializer for Order"""
    class Meta:
        model = Genre
        fields = ("id", "name")
