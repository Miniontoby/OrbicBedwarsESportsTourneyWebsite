# OrbicBedwarsESportsTourneyWebsite

The website code for the Orbic Bedwars E-Sports Tourney.


## Installation

First off, you must clone this repo:
```bash
git clone https://github.com/Miniontoby/OrbicBedwarsESportsTourneyWebsite.git
cd OrbicBedwarsESportsTourneyWebsite
```

Then copy `example.env` to `.env` and edit `.env` to add in:
- a random secret key
- the hypixel api key
- (optional) discord bot token and channel id


Then you must install the dependencies
```bash
pip install -r requirements.txt
```

Then run the app using:
```bash
flask --app main run
```
The app will be listening on `http://localhost:5000`


To make it listen on all ips on port 3000, run this command:
```bash
flask --app main run --host 0.0.0.0 --port 3000
```


## Roadmap

Here's a list of stuff I want to be able to add.
There's a lot more stuff in here to make it more dynamic/generic,
but that's for someone who wants to improve the project for like the [YH4F competition](https://yhf4.org)

- [x] Management of tourney and players
  - [ ] Hoster login
  - [ ] System to create a (new) tourney
  - [ ] Allow changing settings:
    - [ ] How many teams
    - [ ] How many players in team
    - [ ] Available colors for the teams
    - [ ] Signed up players data source (signup form, discord bot, etc.)
    - [ ] Player nickname validator source
    - [ ] Player avatar data source (if applies)
    - [ ] Player stats data source
    - [ ] VDO.Ninja room settings: room name, password, etc.
  - [x] Get a list of people who want to play:
    - [ ] Built-in tourney signup form
    - [x] Discord Bot Integration to read messages with the nicknames from a channel (needs to be with format parser)
  - [ ] Check if the player nickname exists (needs to be dynamic)
  - [x] Getch some stats of the players (needs to be dynamic)
  - [ ] Drag/drop players in and out of the tourney teams (show the stats so the teams can be made fair)
- [ ] Management of teams and scores:
  - [ ] Moderator login
  - [ ] Allow updating scores of the teams
  - [ ] Allow changing the color of the team (since playing multiple rounds and not always being the same color)
  - [ ] Allow updating stats per player (like kills perhaps)
- [ ] Team Dashboard
  - [ ] Per team login, not per player
  - [ ] View team score and the other teams scores
  - [ ] View team color for the next round
  - [ ] Show the per player screenshare links (Powered by VDO.Ninja)
  - [ ] Give streamers a link to the overlay for their POV (if they want to show it on their stream as well)
- [ ] Overlays
  - [x] Show title of tourney
  - [x] Show promotion banner (needs to be dynamic)
  - [ ] Add websocket server for allowing updating the data
  - [ ] Player POV overlay:
    - [x] Nickname
    - [x] Player avatar [if exists]
    - [x] Team name
    - [x] Team color
    - [ ] Team score??
    - ???
  - [ ] Camera POV overlay:
    - [x] Show all teams
    - [x] Show team colors
    - [x] Show team scores
    - ???
  - [ ] Commentary POV overlay:
    - [ ] Make slots for the commentator's faces?
    - [ ] Show team scores?
    - ???

