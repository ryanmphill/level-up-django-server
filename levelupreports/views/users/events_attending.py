"""Module for generating events by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from levelupreports.views.helpers import dict_fetch_all


class UserEventList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all events along with the gamer first name, last name, and id
            db_cursor.execute("""
            SELECT
                e.id AS event_id,
                e.title AS event_title,
                e.date,
                e.game_id,
                e.organizer_id,
                organizer_user.first_name || ' ' || organizer_user.last_name AS organizer_full_name,
                bridge.gamer_id AS attendee_id,
                attendee_user.first_name || ' ' || attendee_user.last_name AS attendee_full_name,
                game.title AS game_title
            FROM levelupapi_eventgamer bridge
            JOIN levelupapi_event e ON e.id = bridge.event_id
            JOIN levelupapi_gamer organizer_gamer ON e.organizer_id = organizer_gamer.id
            JOIN auth_user organizer_user ON organizer_gamer.user_id = organizer_user.id
            JOIN levelupapi_game game ON game.id = e.game_id
            JOIN levelupapi_gamer attendee_gamer ON attendee_gamer.id = bridge.gamer_id
            JOIN auth_user attendee_user ON attendee_gamer.user_id = attendee_user.id 
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            # Take the flat data from the dataset, and build the
            # following data structure for each gamer.
            # This will be the structure of the events_attending list:
            #
            # [
            #   {
            #     "gamer_id": 1,
            #     "full_name": "Molly Ringwald",
            #     "events": [
            #       {
            #         "id": 5,
            #         "date": "2020-12-23",
            #         "time": "19:00",
            #         "game_name": "Fortress America"
            #       }
            #     ]
            #   }
            # ]

            events_attending = []

            for row in dataset:
                # TODO: Create a dictionary called event that includes 
                # the id, event title, date, name of game, and organizer
                # from the row dictionary
                event = {
                    "id": row['event_id'],
                    "title": row['event_title'],
                    "game": row['game_title'],
                    "date": row['date'],
                    "organizer":row['organizer_full_name']
                }
                
                # See if the gamer has been added to the events_attending list already
                user_dict = None
                for user_attending in events_attending:
                     if user_attending['gamer_id'] == row['attendee_id']:
                         user_dict = user_attending
                
                
                if user_dict:
                    # If the user_dict is already in the games_by_user list, append the game to the games list
                    user_dict['events'].append(event)
                else:
                    # If the user is not on the games_by_user list, create and add the user to the list
                    events_attending.append({
                        "gamer_id": row['attendee_id'],
                        "full_name": row['attendee_full_name'],
                        "events": [event]
                    })
        
        # The template string must match the file name of the html template
        template = 'users/list_with_events.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "userevent_list": events_attending
        }

        return render(request, template, context)
