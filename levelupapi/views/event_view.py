"""View module for handling requests about games"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, Event


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
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """
        events = Event.objects.all()

        if "game" in request.query_params:
            game_query =  request.query_params['game']
            events = events.filter(game_id=game_query)


        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized event instance
        """
        organizer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data["game"])

        event = Event.objects.create(
        title=request.data["title"],
        organizer=organizer,
        game=game,
        date=request.data["date"]
        )
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a event

        Returns:
            Response -- Empty body with 204 status code
        """

        event = Event.objects.get(pk=pk)
        event.title = request.data["title"]

        organizer = Gamer.objects.get(pk=request.data["organizer"])
        event.organizer = organizer

        game = Game.objects.get(pk=request.data["game"])
        event.game = game

        event.date = request.data["date"]

        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

class GameOfEventSerializer(serializers.ModelSerializer):
    """JSON serializer for gamer
    """
    class Meta:
        model = Game
        fields = ('id', 'title', 'game_type', 'maker', 'creator')

class EventOrganizerSerializer(serializers.ModelSerializer):
    """JSON serializer for gamer
    """
    class Meta:
        model = Gamer
        fields = ('id', 'user', 'bio', 'full_name')

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """

    game = GameOfEventSerializer(many=False)
    organizer = EventOrganizerSerializer(many=False)

    class Meta:
        model = Event
        fields = ('id', 'title', 'organizer', 'game', 'date', 'attendees')
        depth = 1
