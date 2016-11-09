# Used to make all the databases.
import sqlite3

class DatabaseTools:


	@staticmethod
	def create_database():
		game_list = ["pick3", "pick4", "cash5", "all_or_nothing", 
				 "lucky_for_life", "powerball", "mega_millions"]
		
		for game in game_list:
			conn = sqlite3.connect('databases/{}.db'.format(game))
			cursor = conn.cursor()
			with conn:		
				if game == 'pick3' or 'pick4' or 'all_or_nothing':
					cursor.execute('''
					CREATE TABLE {}(time TEXT, date TEXT, numbers TEXT)
				'''.format(game))

				elif game == 'cash5':
					cursor.execute('''
					CREATE TABLE cash5(date TEXT, numbers TEXT, jackpot TEXT)
				''')

				else:
					cursor.execute('''
					CREATE TABLE {}(date TEXT, numbers TEXT)
				'''.format(game))


	@staticmethod
	def insert_row(database, data):
		conn = sqlite3.connect('databases/{}.db'.format(database))
		cursor = conn.cursor()

		with conn:
			if len(data) == 3:			
				cursor.execute('''
						INSERT INTO {}
						VALUES (?, ?, ?)
				'''.format(database), (data[0], data[1], data[2]))
			elif len(data) == 2:
				cursor.execute('''
						INSERT INTO {}
						VALUES (?, ?)
				'''.format(database), (data[0], data[1]))


if __name__ == '__main__':
	create_database()
