import argparse
import sys
import pandas as pd
import re
import os


'''Args'''
def get_args(command_line_arguments):
	parser = argparse.ArgumentParser(description="find club and international squad players of a certain football "
												 "player",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter,  # include defaults in help
                                     conflict_handler='resolve')  # allows overridng of arguments

	# Input params
	parser.add_argument("-f", "--folder", default=None,
						help="the folder where the csvs are kept")
	parser.add_argument("-p1", "--player_one", default='Steed Malbranque',
                        help="the player you want to match against player two")
	parser.add_argument("-p2", "--player_two", default='Lionel Messi',
						help="the player you want to match against player one")
	parser.add_argument("-t", "--type", choices=('both', 'club', 'nation'), default='both',
						help="matches for both club and nation, or club or nation")

	args = parser.parse_args(command_line_arguments)

	return args


def main(supplied_args):
	args = get_args(supplied_args)

	player_one_name_save = re.sub('[^A-Za-z0-9]+', '', args.player_one).lower()
	player_one_file = f'{player_one_name_save}-squadmates.csv'

	player_two_name_save = re.sub('[^A-Za-z0-9]+', '', args.player_two).lower()
	player_two_file = f'{player_two_name_save}-squadmates.csv'

	player_one = pd.read_csv(os.path.join(args.folder,player_one_file))
	player_two = pd.read_csv(os.path.join(args.folder, player_two_file))

	if args.type != 'both':
		player_one = player_one[player_one.type == args.type]
		player_two = player_two[player_two.type == args.type]

	matches = [x for x in player_one.player.to_list() if x in set(player_two.player.to_list())]
	matches = set(matches)

	print(f'\nPlayers who have played with {args.player_one} and {args.player_two} are:\n')
	print(*matches, sep='\n')


if __name__ == '__main__':
	main(sys.argv[1:])