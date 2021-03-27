from django.shortcuts import render

from rest_framework import generics, status
from .serializers import RoomSerializer, CreateRoomSerializer
from .models import Room
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
# creates the backend APi view here 

class RoomView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class =  RoomSerializer
    
# Api views allows us to override some default methods like get, post 
class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer
    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        # Give python representation of our data and checks if data ebing sent is valid 
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause') 
            votes_to_skip = serializer.data.get('votes_to_skip')
           # time_created = serializer.data.get('time_created')
            host = self.request.session.session_key
            queryset = Room.objects.filter(host=host)
            # Checking if the user has an existing music room already created
            #In that case, update this room with the settings
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                #room.time_created = time_created
                # add time_created to the list below
                room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
                #serilazing the response
                return Response(RoomSerializer(room).data, status.HTTP_200_OK)
            else:
                room = Room(host=host, guest_can_pause=guest_can_pause, votes_to_skip=votes_to_skip)
                room.save()
                return Response(RoomSerializer(room).data, status.HTTP_201_CREATED)

        return Response({'Bad Request' : 'Invalid Data...'}, status=status.HTTP_400_BAD_REQUEST)