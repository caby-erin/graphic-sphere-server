from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import action
from graphicsphereapi.models import Novel, User, NovelGenre, Genre, Review

class NovelView(ViewSet):
  
  
  @action(methods=['post'], detail=True)
  def add_genre_to_novel(self, request, pk):
      novel = Novel.objects.get(pk=pk)
      genre = Genre.objects.get(id=request.data['genreId'])
      try:
        NovelGenre.objects.get(novel=novel, genre=genre)
        return Response({'message: This novel already has this genre.'})
      except NovelGenre.DoesNotExist:
        NovelGenre.objects.create(
            novel=novel,
            genre=genre
        )
        return Response(None, status=status.HTTP_200_OK)

  @action(methods=['delete'], detail=True)
  def remove_genre_from_novel(self, request, pk):
      novel = Novel.objects.get(pk=pk)
      novel_genre = NovelGenre.objects.get(novel=novel, genre=request.data['genreId'])
      novel_genre.delete()

      return Response(None, status=status.HTTP_200_OK)
  
  def retrieve (self, request, pk):
    novel = Novel.objects.get(pk=pk)
    serializer = NovelSerializer(novel)
    return Response(serializer.data)

  def list(self, request):
    novels = Novel.objects.all()
    user = request.query_params.get('user', None)
    if user is not None:
      novels = novels.filter(user=user)
    serializer = NovelSerializer(novels, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  # @action(detail=False, methods=['get'])
  # def filter_by_genre(self, request):
  #       genre_id = request.query_params.get('genre_id', None)
  #       if not genre_id:
  #           return Response({'message': 'GEnre ID parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

  #       novels = Novel.objects.filter(genres__genre__id=genre_id)
  #       serializer = NovelSerializer(novels, many=True)
  #       return Response(serializer.data, status=status.HTTP_200_OK)
  
  
  def create(self, request):
    user = User.objects.get(pk=request.data["userId"])
    
    novel = Novel.objects.create(
      user = user,
      title = request.data["title"],
      image_url=request.data["imageUrl"],
      description = request.data["description"],
      rating = request.data["rating"]
    )
    
    novel.save()
    serializer = NovelSerializer(novel)
    return Response(serializer.data)
  
  def update(self, request, pk):
    novel = Novel.objects.get(pk=pk)
    novel.title=request.data["title"]
    novel.image_url=request.data["imageUrl"]
    novel.description = request.data["description"]
    novel.rating = request.data["rating"]
  
    novel.save()
    return Response(None, status=status.HTTP_200_OK)
  
  def destroy(self, request, pk):
    novel = Novel.objects.get(pk=pk)
    novel.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)

class NovelGenreSerializer(serializers.ModelSerializer):
  id = serializers.ReadOnlyField(source='genre.id')
  name = serializers.ReadOnlyField(source='genre.name')
  class Meta:
    model = NovelGenre
    fields = ('id', 'name')
    
class NovelReviewSerializer(serializers.ModelSerializer):
  class Meta:
    model= Review
    fields=('id','user','content')
    depth = 1
class NovelSerializer(serializers.ModelSerializer):
  genres = NovelGenreSerializer(many=True, read_only=True)
  reviews = NovelReviewSerializer(many=True, read_only=True)
  class Meta:
    model = Novel
    fields = ('id', 'user', 'title', 'image_url', 'description', 'reviews', 'genres')
    depth = 1
