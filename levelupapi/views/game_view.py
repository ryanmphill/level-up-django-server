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
        response_body = {}
        status_code = status.HTTP_200_OK
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            response_body = serializer.data
        except Game.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
        return Response(response_body, status=status_code)


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
    
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]

        game_type = GameType.objects.get(pk=request.data["game_type"])
        game.game_type = game_type

        game.maker = request.data["maker"]

        creator = Gamer.objects.get(pk=request.data["creator"])
        game.creator = creator

        game.number_of_players = request.data["number_of_players"]
        game.skill_level = request.data["skill_level"]

        
        game.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        """Handle DELETE requests

        Returns:
            Response -- Empty body with 204 status code
        """
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        


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
