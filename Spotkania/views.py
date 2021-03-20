from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from Spotkania.serializers import *
from Spotkania.models import Meet
from rest_framework.response import Response

class MeetingViewSetList(APIView):

    def get(self,format=None):
        queryset = Meet.objects.all()
        serializer = MeetingSerializer(queryset,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = MeetingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class MeetingViewSetDetail(APIView):
    def get_object(self,pk):
        try:
            return Meet.objects.get(id_meet=pk)
        except Meet.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset=self.get_object(pk)
        serializer = MeetingSerializer(queryset)
        return Response(serializer.data)

    def put(self,request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = MeetingSerializer(queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk=None, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self,request,pk=None,format=None):
        queryset = self.get_object(pk)
        serializer = MeetingSerializer(queryset,data=request.data,prtaial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
