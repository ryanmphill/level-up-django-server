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

class GameOfEventSerializer(serializers.ModelSerializer):
    """JSON serializer for gamer
    """
    class Meta:
        model = Game
        fields = ('id', 'name', 'game_type', 'creator')

class EventOrganizerSerializer(serializers.ModelSerializer):
    """JSON serializer for gamer
    """
    class Meta:
        model = Gamer
        fields = ('id', 'user', 'bio')

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """

    game = GameOfEventSerializer(many=False)
    organizer = EventOrganizerSerializer(many=False)

    class Meta:
        model = Event
        fields = ('id', 'title', 'organizer', 'game', 'date', 'attendees')
        depth = 1
