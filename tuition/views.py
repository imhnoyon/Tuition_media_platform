from django.shortcuts import render
from rest_framework import viewsets
from .models import Tuition,Review
from .serializer import TuitionSerializer,ReviewSerializer
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status

# class TuitionViewset(viewsets.ModelViewSet):
#     queryset=Tuition.objects.all()
#     serializer_class=TuitionSerializer


class TuitionViewset(APIView):
    def get(self, request, format=None):
        Tuitions = Tuition.objects.all()
        serializer = TuitionSerializer(Tuitions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TuitionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ReviewViewset(viewsets.ModelViewSet):
#     queryset=Review.objects.all()
#     serializer_class=ReviewSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['tuition']


class ReviewViewset(APIView):
    def get(self, request, format=None):
        Reviews = Review.objects.all()
        serializer = ReviewSerializer(Reviews, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TuitionDetail(APIView):  
    def get_object(self, pk):
        try:
            return Tuition.objects.get(pk=pk)
        except Tuition.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        tuition = self.get_object(pk)
        serializer = TuitionSerializer(tuition)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        tuition = self.get_object(pk)
        serializer = TuitionSerializer(tuition, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        tuition = self.get_object(pk)
        tuition.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class TuitionList(APIView):
   
    def get(self, request, format=None):
     
        tuitions = Tuition.objects.all()
        serializer = TuitionSerializer(tuitions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        
        print(request.data)
        serializer = TuitionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)