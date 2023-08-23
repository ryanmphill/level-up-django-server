SELECT
    e.id,
    e.title,
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
JOIN auth_user attendee_user ON attendee_gamer.user_id = attendee_user.id;