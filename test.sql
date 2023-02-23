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