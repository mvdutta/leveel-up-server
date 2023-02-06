"""View module for handling requests about events"""
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
        fields = ('id', 'game', 'organizer', 'event_date', 'event_time', 'description')
        depth = 1

