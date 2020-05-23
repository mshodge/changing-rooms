# changing-rooms

A simple python script that crawls [www.worldfootball.net](www.worldfootball.net) to find squad mates of a requested player.

### Requires

- beautifulsoup4
- requests
- pandas
- unidecode

### Basic run

Type `python changing-rooms.py -p <player_name>` into your terminal. Default player is the Fulham legend `Steed Malbranque`.

### Examples

See `/examples` for CSV files for Cristiano Ronaldo, Lionel Messi, Roberto Carlos and of course, Steed Malbranque (see table example below).

|player|team                         |season|
|------|-----------------------------|------|
|Christophe Breton|Olympique Lyon               |1997-1998|
|Gregory Coupet|Olympique Lyon               |1997-1998|
|Ghislain Anselmini|Olympique Lyon               |1997-1998|
|Jacek Bak|Olympique Lyon               |1997-1998|
|Olivier Bellisi|Olympique Lyon               |1997-1998|
|Patrice Carteron|Olympique Lyon               |1997-1998|


### Rules

Please use responsibly on [www.worldfootball.net](www.worldfootball.net). They provide a brilliant free service, don't exploit that.

### To do

- Add national teams.