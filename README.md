# changing-rooms

A simple python script that crawls [www.worldfootball.net](www.worldfootball.net) to find squad mates of a requested player (both club and national (senior)).

## Step-by-step Guide

### 1. Install Python

You will need Python 3. The easiest way is to use Anaconda. Here is the [official installation guide](https://docs.anaconda.com/anaconda/install/).


### 2. Clone this code

Type `cd <path>` in your command line, where `<path>` is your chosen folder.

Use `git clone https://github.com/mshodge/changing-rooms.git` in your command line to clone it locally to the folder.

Type `cd changing-rooms` to enter the folder in your command line.

### 3. Install Dependencies

The code requires the following packages:

- beautifulsoup4
- requests
- pandas
- unidecode

To install run `conda install -r requirements.txt` in the `changing-rooms` folder.

### 4. Basic Code Example

Type `python changing-rooms.py -p <player_name>` into your terminal. Default player is the Fulham legend `Steed Malbranque`.

As it runs it will print some information to the command line.

A comma separated (CSV) file will be saved to the `changing-rooms` folder. You can open this in Excel now.

The CSV file will have the following headers:

- player (the name of the squad mate)
- team (the team)
- season (the season, e.g. 2000-2001)
- type (club or nation)

## Provided Examples

See `/examples` for CSV files for a number of world famous players including Steed Malbranque.

## Rules

Please use responsibly on [www.worldfootball.net](www.worldfootball.net). They provide a brilliant free service, don't exploit that.