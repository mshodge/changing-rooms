import argparse
import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
import unidecode
import re


'''Args'''
def get_args(command_line_arguments):
	parser = argparse.ArgumentParser(description="find club and international squad players of a certain football "
												 "player",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter,  # include defaults in help
                                     conflict_handler='resolve')  # allows overridng of arguments

	# Input params
	parser.add_argument("-p", "--player", default='Steed Malbranque',
                        help="the player you want to find squad mates of")

	args = parser.parse_args(command_line_arguments)

	return args


'''Find National Team URL'''
def find_national_team_url(args, nation):

	player_url = args.player.lower().replace(' ', '-')
	international_history = f'https://www.worldfootball.net/player_summary/{player_url}/4/'
	page = requests.get(international_history)
	soup = BeautifulSoup(page.content, 'html.parser')

	paths = soup.findAll('a', href=True, text=re.compile(nation))

	for path in paths:
		if path.attrs.get('href')[0:5] == '/team':
			nation_url = path.attrs.get('href')
			break

	return nation_url


'''Find Player's Club History'''
def player_club_history(args):

	player_url = args.player.lower().replace(' ','-')
	player_history = f'https://www.worldfootball.net/player_summary/{player_url}/'
	page = requests.get(player_history)
	soup = BeautifulSoup(page.content, 'html.parser')

	teams = []
	teams_url = []
	years_start = []
	years_end = []

	still_playing = False

	'''Finds current team if the player is still playing'''
	try:
		current_team = soup.findAll("td", {"width": "60%"})[0].findAll("a")
		if current_team[0].string[0] != '1' and current_team[0].string[0] != '2':
			teams.append(str(current_team[0].string))
			teams_url.append(current_team[0].attrs.get('href'))
			still_playing = True
	except IndexError:
		None


	'''Finds nation of player'''
	try:
		nation = str(soup.findAll("span", {"itemprop": "nationality"})[0].string)
	except IndexError:
		print('\nAborting: Player not in database. Please check name is spelt correctly\n')
		sys.exit()

	'''Gets career years'''
	years_table = soup.findAll("td", {"width": "20%"})
	for year_table in years_table:
		try:
			if '-' in year_table.string:
				years_start.append(int(''.join(year_table.string.split())[3:7]))
				years_end.append(int(''.join(year_table.string.split())[11:15]))
		except (ValueError, TypeError):
			continue

	'''Finds teams'''
	teams_table = soup.findAll("td", {"width": "40%"})
	for team_table in teams_table:
		if str(team_table.string)[0] != '\n':
			teams.append(str(team_table.string))
			teams_url.append(team_table.contents[0].attrs.get('href'))

	teams = teams[::-1]
	teams_url = teams_url[::-1]
	years_start = years_start[::-1]
	years_end = years_end[::-1]

	years_start = years_start + [years_end[len(years_end) - 1]]
	years_end = years_end + [(years_end[len(years_end) - 1] + 1)]

	if still_playing == True:
		years_end[-1] = 2020

	return teams, teams_url, years_start, years_end, nation


'''Finds national squad mates of the player'''
def find_national_mates(args, nation, nation_url, years_start, years_end):

	player = []
	club = []
	season = []
	type = []

	print('\n----Retrieving National Team Information-----\n')

	for i in range(years_start[0] + 1, years_end[-1] + 1):
		print(f'Getting national squad mates for {args.player} for {nation} during the {i-1}-{i} season')
		squad_url = f'https://www.worldfootball.net{nation_url}freundschaft-{i}/2/'
		page = requests.get(squad_url)
		soup = BeautifulSoup(page.content, 'html.parser')
		players_table = soup.findAll("a")
		for player_table in players_table:
			try:
				if str(player_table.attrs.get('href')[0:3]) == '/pl':
					player_found = str(player_table.attrs.get('title'))
					player_found = unidecode.unidecode(player_found)
					player.append(player_found)
					club.append(nation)
					season.append(f'{i-1}-{i}')
					type.append('nation')
			except TypeError:
				continue

	return player, club, season, type


'''Finds club mates of the player'''
def find_club_mates(args, teams, teams_url, years_start, years_end):

	player = []
	club = []
	season = []
	type = []

	print('\n----Retrieving Club Team Information-----\n')

	for team in teams:

		idx = teams.index(team)

		for i in range(years_start[idx] + 1, years_end[idx] + 1):
			print(f'Getting club squad mates for {args.player} for {teams[idx]} during the {i-1}-{i} season')
			squad_url = f'https://www.worldfootball.net{teams_url[idx]}{i}/2/'
			page = requests.get(squad_url)
			soup = BeautifulSoup(page.content, 'html.parser')
			players_table = soup.findAll("a")
			for player_table in players_table:
				try:
					if str(player_table.attrs.get('href')[0:3]) == '/pl':
						player_found = str(player_table.attrs.get('title'))
						player_found = unidecode.unidecode(player_found)
						player.append(player_found)
						club.append(team)
						season.append(f'{i-1}-{i}')
						type.append('club')
				except TypeError:
					continue

		'''Removes club incase the player has played for the same club more than once at two points in their career'''
		teams[idx] = 'Searched'

	return player, club, season, type


def print_summary(args, player, team, season):
	print(f' \n{args.player}:\n\n '
		  f'- Has played for {len(set(team)) - 1} clubs \n'
		  f' - Has had {len(set(player)) - 1} different squad mates \n'
		  f' - Has played across {len(set(season))} seasons \n')


def save_results(args, player, team, season, type):
	df = pd.DataFrame({'player': player, 'team': team, 'season': season, 'type': type})
	df = df.drop_duplicates()
	df = df[df.player != args.player]
	player_name_save = re.sub('[^A-Za-z0-9]+', '', args.player).lower()
	df.to_csv(f'{player_name_save}-clubmates.csv', index=False)


def main(supplied_args):
	args = get_args(supplied_args)
	teams, teams_url, years_start, years_end, nation = player_club_history(args)
	nation_url = find_national_team_url(args, nation)
	club_player, club_team, club_season, club_type = find_club_mates(args, teams, teams_url, years_start, years_end)
	nation_player, nation_team, nation_season, nation_type = find_national_mates(args, nation, nation_url, years_start, years_end)

	player = club_player + nation_player
	team = club_team + nation_team
	season = club_season + nation_season
	type = club_type + nation_type

	print_summary(args, player, team, season)
	save_results(args, player, team, season, type)


if __name__ == '__main__':
	main(sys.argv[1:])