SELECT P.trophies, CM.clan_tag
FROM db.player AS P
JOIN db.clan_member AS CM ON P.player_tag = CM.player_tag;