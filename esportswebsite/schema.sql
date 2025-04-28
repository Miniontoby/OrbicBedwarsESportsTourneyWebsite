-- Initialize the database.
-- Drop any existing data and create tables and add standard data.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS player;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS color;

CREATE TABLE color (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL
);

INSERT INTO color (id, name) VALUES
  (1, 'red'),
  (2, 'blue'),
  (3, 'green'),
  (4, 'yellow'),
  (5, 'aqua'),
  (6, 'white'),
  (7, 'pink'), 
  (8, 'gray');

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL
);

CREATE TABLE team (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  color_id INTEGER NOT NULL,
  score INTEGER NOT NULL DEFAULT 0,
  username TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL DEFAULT '',
  FOREIGN KEY (color_id) REFERENCES color (id)
);

INSERT INTO team (id, color_id, score, username, password) VALUES
  (1, 1, 0, 'TeamAlpha', ''),
  (2, 2, 0, 'BetaTeam', ''),
  (3, 3, 0, 'TripleMasters', ''),
  (4, 4, 0, 'CookingFours', '');

CREATE TABLE player (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nickname TEXT UNIQUE NOT NULL,
  rank TEXT DEFAULT NULL,
  bedwarsLevel INTEGER DEFAULT NULL,
  team_id INTEGER NULL DEFAULT NULL,
  FOREIGN KEY (team_id) REFERENCES team (id)
);

INSERT INTO player (id, nickname, team_id) VALUES
  (1, 'xFlxme', 1),
  (2, 'Sololad', 1),
  (3, 'DrBoolFliker', 1),
  (4, 'Mang0sorbet', 1),
  (5, 'oCxmboo', 2),
  (6, 'RedMiniontoby', 2),
  (7, 'LeoNoche', 2),
  (8, 'TheTrueCheeseMan', 2),
  (9, 'RealSuper', 3),
  (10, 'Akmatras', 3),
  (11, 'MindaMann', 3),
  (12, 's3conds', 3),
  (13, 'uDeath', 4),
  (14, 'AnxiousPiggy', 4),
  (15, 'SOMEBLANKET', 4),
  (16, 'xReefed', 4),
  (17, 'RedMiniontoby2', NULL);
