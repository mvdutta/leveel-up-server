 SELECT
    g.id,
    g.game_title,
    g.maker,
    g.type_id,
    g.creator_id,
    g.skill_level, 
    g.num_of_players,
    u.id,
    u.first_name || " " || u.last_name AS [Full Name]
FROM levelupapi_game g
JOIN levelupapi_gamer gm ON g.id = gm.id
JOIN auth_user u ON gm.user_id = u.id   


 SELECT
    e.id,
    e.description,
    e.game_id,
    e.organizer_id,
    e.event_time,
    e.event_date,
    g.game_title AS game_name,
    u.first_name || " " || u.last_name AS full_name
FROM levelupapi_event e
JOIN levelupapi_game g ON g.id = e.game_id
JOIN levelupapi_gamer gm ON gm.id = e.organizer_id
JOIN auth_user u ON gm.user_id = u.id   