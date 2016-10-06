#http://www.powerball.com/powerball/winnums-text.txt
#http://data.ny.gov/resource/d6yy-54nr.json
#https://data.ny.gov/Government-Finance/Lottery-Mega-Millions-Winning-Numbers-Beginning-20/5xaw-6ayf
import re
import urllib2

from bs4 import BeautifulSoup

game_links = {
	'pick3_mid_day': 'http://www.lotteryusa.com/north-carolina/midday-3/year',
	'pick3_evening': 'http://www.lotteryusa.com/north-carolina/pick-3/year',
	'pick4_mid_day': 'http://www.lotteryusa.com/north-carolina/midday-pick-4/year',
	'pick4_evening': 'http://www.lotteryusa.com/north-carolina/pick-4/year',
	'cash5': 'http://www.lotteryusa.com/north-carolina/cash-5/year',
	'aor_mid_day': 'http://www.lotteryusa.com/north-carolina/midday-all-or-nothing/year',
	'aor_evening': 'http://www.lotteryusa.com/north-carolina/night-all-or-nothing/year',
	'mega_millions': 'http://www.lotteryusa.com/north-carolina/mega-millions/year',
	'powerball': 'http://www.powerball.com/powerball/winnums-text.txt',
	'lucky_4_life': 'http://www.lotteryusa.com/north-carolina/lucky-4-life/year'
}

def makesoup(url):
	"""
		Request the page and parse the infromation
	   	to return a soup object.
	"""
	req = urllib2.Request(url)
	page = urllib2.urlopen(req)
	soup = BeautifulSoup(page.read(), 'html.parser')
	return soup

def pick3(url, time):
	try:
		print "[Attempt] Pick 3 '{}'".format(time)
		get_date = makesoup(url).find_all('td', {'class': 'date'})
		get_numbers = makesoup(url).find_all('td', {'class': 'result'})
	except:
		print "[Error] Pick 3 '{}'".format(time)
		return

	date_list = [line.text for line in get_date]
	number_list = []
	
	for line in get_numbers:
		#This is the data structure: u'\n6\n6\n0\n0\n\n'
		line = re.sub('\n', ',', line.text[1:], 2)
		#This is what we're working with now: 
		#u'2,6,14,31,38\n\n'
		line = re.sub('\n', '', line)
		number_list.append(line)

	if time == 'day':
		drawing_time = ["D" for item in range(len(date_list))]
		pick3_list = zip(drawing_time, date_list, number_list)
	elif time == 'evening':
		drawing_time = ["E" for item in range(len(date_list))]
		pick3_list = zip(drawing_time, date_list, number_list)
	else:
		raise ValueError("Time must be either day or evening, got '{}'".format(
				time))
	print pick3_list

def pick4(url, time):
	try:
		print "[Attempt] Pick 4 '{}'".format(time)
		get_date = makesoup(url).find_all('td', {'class': 'date'})
		get_numbers = makesoup(url).find_all('td', {'class': 'result'})
	except:
		print "[Error] Pick 4 '{}'".format(time)
		return

	date_list = [line.text for line in get_date]
	number_list = []
	
	for line in get_numbers:
		#This is the data structure: u'\n6\n6\n0\n0\n\n'
		line = re.sub('\n', ',', line.text[1:], 3)
		#This is what we're working with now: 
		#u'2,6,14,31,38\n\n'
		line = re.sub('\n', '', line)
		number_list.append(line)

	if time == 'day':
		drawing_time = ["D" for item in range(len(date_list))]
		pick4_list = zip(drawing_time, date_list, number_list)
	elif time == 'evening':
		drawing_time = ["E" for item in range(len(date_list))]
		pick4_list = zip(drawing_time, date_list, number_list)
	else:
		raise ValueError("Time must be either day or evening, got '{}'".format(
				time))
	print pick4_list

def cash5(url):
	try:
		print "[Attempt] Cash 5"
		get_date = makesoup(url).find_all('td', {'class': 'date'})
		get_numbers = makesoup(url).find_all('td', {'class': 'result'})
		get_jackpot = makesoup(url).find_all('td', {'class': 'jackpot'})
	except:
		print "[Error] Cash 5"
		return 

	date_list = [line.text for line in get_date]
	jackpot_list = [line.text for line in get_jackpot]
	number_list = []

	for line in get_numbers:
		#This is the data structure: u'\n2\n6\n14\n31\n38\n\n'
		line = re.sub('\n', ',', line.text[1:], 4)
		#This is what we're working with now: 
		#u'2,6,14,31,38\n\n'
		line = re.sub('\n', '', line)
		number_list.append(line)

	cash5_list = zip(date_list, number_list, jackpot_list)
	#(u'Thu, Oct 22, 2015', u'7,21,24,27,30', u'$60,000')
	print "[Sucess] Cash 5"
	print cash5_list
	
def all_or_nothing(url, time):
	try:
		print "[Attempt] All or Nothing '{}'".format(time)
		get_date = makesoup(url).find_all('td', {'class': 'date'})
		get_numbers = makesoup(url).find_all('td', {'class': 'result'})
	except:
		print "[Error] All or Nothing '{}'".format(time)
		return

	date_list = [line.text for line in get_date]
	number_list = []

	for line in get_numbers:
		#This is the data structure: 
		#u'\n3\n4\n6\n7\n9\n10\n11\n15\n17\n20\n23\n24\n\n'
		line = re.sub('\n', ',', line.text[1:], 11)
		#This is what we're working with now: 
		#u'3,6,7,9,10,11,15,17,20,23,24\n\n'
		line = re.sub('\n', '', line)
		number_list.append(line)

	if time == 'day':
		drawing_time = ["D" for item in range(len(date_list))]
		aor_list = zip(drawing_time, date_list, number_list)
	elif time == 'evening':
		drawing_time = ["E" for item in range(len(date_list))]
		aor_list = zip(drawing_time, date_list, number_list)
	else:
		raise ValueError("Time must be either day or evening, got '{}'".format(
				time))

	print "[Sucess] All or Nothing '{}'".format(time) 

def powerball(url):
	try:
		print "[Attempt] Powerball"
		soup = makesoup(url)
	except:
		print "[Error] Powerball"
		return
	
	date_list = []
	number_list = []
	
	for line in soup:
		#Data structure: 
		#10/01/2016  12  64  50  61  02  01  2
		date = re.findall('\d\d/\d\d/\d{4}', line)
		number = re.sub('\d\d/\d\d/\d{4}', '', line)
		number = re.sub('\r\n', ',', number)
		number_list.append(number)
	print number_list
		#date_list.append(date)
def main():
	pick3_url_mid_day = game_links.get('pick3_mid_day')
	pick3_url_evening = game_links.get('pick3_evening')
	pick4_url_mid_day = game_links.get('pick4_mid_day')
	pick4_url_evening = game_links.get('pick4_evening')
	cash5_url = game_links.get('cash5')
	aor_url_mid_day = game_links.get('aor_mid_day')
	aor_url_evening = game_links.get('aor_evening')
	mega_millions_url = game_links.get('mega_millions')
	powerball_url = game_links.get('powerball')
	lucky_4_life_url = game_links.get('lucky_4_life')
	print powerball(powerball_url)

if __name__ == '__main__':
	main()
