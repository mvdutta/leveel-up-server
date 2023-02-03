"""View module for handling requests about games"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer


class GameView(ViewSet):
    """Level up game types view"""

    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single ticket
            Returns:
            Response -- JSON serialized ticket record
        """

        game = Game.objects.get(pk=pk)
        serialized = GameSerializer(
            game, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)


class CreatorSerializer(serializers.ModelSerializer):
    """JSON serializer for creator on games"""
    class Meta:
        model = Gamer
        fields = ('id', 'bio', 'full_name',)


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    creator = CreatorSerializer(many=False)
    class Meta:
        model = Game
        fields = ('id', 'game_title', 'type', 'creator', 'skill_level', 'maker', 'num_of_players')
        depth = 1