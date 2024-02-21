from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from graphicsphereapi.models import Review, User, Novel

class ReviewView(ViewSet):
  def retrieve(self, request, pk):
    try:
        review = Review.objects.get(pk=pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    except review.DoesNotExist as ex:
        return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

  def list(self, request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)
  
  def create(self, request):
      user = User.objects.get(pk=request.data["userId"])
      novel = Novel.objects.get(pk=request.data["novelId"])

      review = Review.objects.create(
        user = user,
        novel = novel,
        content=request.data["content"],
      )

      serializer = ReviewSerializer(review)
      return Response(serializer.data)
  
  def update(self, request, pk):
      review = Review.objects.get(pk=pk)
      review.content = request.data["content"]
      review.save()

      return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def destroy(self, request, pk):
      review = Review.objects.get(pk=pk)
      review.delete()
      return Response(None, status=status.HTTP_204_NO_CONTENT)

class ReviewSerializer(serializers.ModelSerializer):
  """JSON serializer for reviews"""
  class Meta:
    model = Review
    fields = ('id', 'user', 'novel', 'content')
    depth = 1
