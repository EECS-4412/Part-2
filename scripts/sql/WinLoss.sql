-- Finds win/loss ratio per team per year
SELECT TEAM_NAME_HOME as TEAM_NAME,
       count(WL_HOME) as HOME_WL,
       count(CASE WHEN WL_HOME = 'W' THEN 1 END) as HOME_WINS,
       count(CASE WHEN WL_HOME = 'L' THEN 1 END) as HOME_LOSES,
       ROUND(
           (CAST(count(CASE WHEN WL_HOME = 'W' THEN 1 END) as FLOAT) / CAST(count(WL_HOME) as FLOAT)) * 100,
           2
       ) as WL_RATIO,
       SUBSTR(Game.GAME_DATE, 0, 5) as YEAR
FROM Game
GROUP BY TEAM_NAME_HOME, Year
