"""View module for handling requests about games"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, GameType, Gamer


class GameView(ViewSet):
    """Level up games view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game
        """
        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        creator = Gamer.objects.get(user=request.auth.user)
        game_type = GameType.objects.get(pk=request.data["game_type"])

        game = Game.objects.create(
        title=request.data["title"],
        game_type=game_type,
        maker=request.data["maker"],
        creator=creator,
        number_of_players=request.data["number_of_players"],
        skill_level=request.data["skill_level"]
        )
        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class GameTypeOfGameSerializer(serializers.ModelSerializer):
    """JSON serializer for gametype
    """
    class Meta:
        model = GameType
        fields = ('id', 'label')

class GameCreatorSerializer(serializers.ModelSerializer):
    """JSON serializer for gamer
    """
    class Meta:
        model = Gamer
        fields = ('id', 'user', 'bio', 'full_name', 'username')

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """

    game_type = GameTypeOfGameSerializer(many=False)
    creator = GameCreatorSerializer(many=False)

    class Meta:
        model = Game
        fields = ('id', 'title', 'game_type', 'maker', 'creator', 'number_of_players', 'skill_level')
        depth = 1
