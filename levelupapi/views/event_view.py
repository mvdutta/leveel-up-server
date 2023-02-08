"""View module for handling requests about events"""
from rest_framework.decorators import action
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game


class EventView(ViewSet):
    """Level up events view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event
        """
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all event

        Returns:
            Response -- JSON serialized list of events
        """
        events = Event.objects.all()
        gamer = Gamer.objects.get(user=request.auth.user)

        for event in events:
            # Check to see if the gamer is in the attendee list on the event
            event.joined = gamer in event.attendee.all()

        #filtering events by game
        if "game" in request.query_params:
            events = events.filter(game = request.query_params['game'])
        

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized event instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data["game"])
        

        event = Event.objects.create(
            game= game,
            organizer=gamer,
            event_date=request.data["event_date"],
            event_time=request.data["event_time"],
            description=request.data["description"] 
        )
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for an event

        Returns:
            Response -- Empty body with 204 status code
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data["game"])

        event = Event.objects.get(pk=pk)
        event.organizer = gamer
        event.event_date = request.data["event_date"]
        event.event_time = request.data["event_time"]
        event.description = request.data["description"]
        event.game = game
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle DELETE requests for events

        Returns:
            Response: None with 204 status code
        """
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""

        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendee.add(gamer)
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Delete request for a user to leave for an event"""
    
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendee.remove(gamer)
        return Response({'message': 'Gamer removed'}, status=status.HTTP_204_NO_CONTENT)

class OrganizerSerializer(serializers.ModelSerializer):
    """JSON serializer for creator on games"""
    class Meta:
        model = Gamer
        fields = ('id', 'bio', 'full_name',)

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    organizer = OrganizerSerializer(many=False)
    class Meta:
        model = Event
        fields = ('id', 'game', 'organizer', 'event_date', 'event_time', 'description', 'attendee', 'joined')
        depth = 1

