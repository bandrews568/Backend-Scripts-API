import re
import urllib2

from bs4 import BeautifulSoup

game_links = {
	'pick3_mid_day': 'http://www.lotteryusa.com/north-carolina/midday-3/year',
	'pick3_evening': 'http://www.lotteryusa.com/north-carolina/pick-3/year',
	'pick4_mid_day': 'http://www.lotteryusa.com/north-carolina/midday-pick-4/year',
	'pick4_evening': 'http://www.lotteryusa.com/north-carolina/pick-4/year',
	'cash5': 'http://www.lotteryusa.com/north-carolina/cash-5/year',
	#aor is an acronym for All or Nothing
	'aor_mid_day': 'http://www.lotteryusa.com/north-carolina/midday-all-or-nothing/year',
	'aor_evening': 'http://www.lotteryusa.com/north-carolina/night-all-or-nothing/year',
	'mega_millions': 'http://www.lotteryusa.com/north-carolina/mega-millions/year',
	'powerball': 'http://www.lottertopicyusa.com/north-carolina/powerball/year',
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

def insert_comma(data, game=None):
	"""
		Add in a comma between the year and lottery #'s
	"""
	if game == 'cash5':
		if "$" in data:
			data = data.split("$")
			new_data = data[0] + ",$" + data[1]
			new_data = new_data[:17] + "," + new_data[17:]
			return new_data
	return data[:17]+ "," + data[17:]

def clean_data(list_name, game=None):
	"""
		Clean the data and return a list.
		After we parse the page Beautiful Soup returns all 
		tables rows in a list in the following format:
			u'Sun, Sep 27, 2015\n3\n2\n3\n\n$500'
		So we have to clean the data to remove the newlines and 
		also take out the jackpot since the jackpot 
		for all pick3 drawings is always $500.
	"""
	if not isinstance(list_name, list):
		raise TypeError("List name must be of <Type: list>")

	cleaned_list = []
	
	for line in list_name:
		#Sub out jackpot amount
		if game == 'pick3':
			cleaned_data = re.sub('\$\d*$', '', line)
		elif game == 'pick4':
			cleaned_data = re.sub('\$\d,\d*$', '', line)
		elif game == 'aor':
			cleaned_data = re.sub('\$\d*,\d*$', '', line)
		#Sub out \n
		cleaned_data = cleaned_data.replace('\n', '')

		if game == 'cash5':			
			cleaned_data = insert_comma(cleaned_data, game='cash5')
		else: 
			cleaned_data = insert_comma(cleaned_data)

		if cleaned_data.startswith("google"):
			continue
		
		if " " in cleaned_data:
			#Take out spaces
			cleaned_data = cleaned_data.replace(' ', '')
		cleaned_list.append(cleaned_data)	
	return cleaned_list

def day_or_evening(list_name, time=None):
	"""
		Add either "D" or "E" to the beginning of each item
		to signify the time of the drawing. 
	"""
	if time == 'day':
		cleaned_list = ["D," + item for item in list_name]
	else:
		cleaned_list = ["E," + item for item in list_name]	
	return cleaned_list

def pick3(url, time=None):
	"""
		returns Type: list
	"""
	soup = makesoup(url).find_all('tr')
	unclean_pick3_list = []

	del unclean_pick3_list[0]
	
	for line in soup:
		unclean_pick3_list.append(line.text)
	
	clean_pick3_list = clean_data(unclean_pick3_list, game='pick3')
	
	if time == 'day':
		clean_pick3_list = day_or_evening(clean_pick3_list, time='day')
	elif time == 'evening':
		clean_pick3_list = day_or_evening(clean_pick3_list, time='evening')
	else:
		raise ValueError("Time must be either day or evening, got '{}'".format(
				time))	
	
	del unclean_pick3_list
	return clean_pick3_list

def pick4(url, time=None):
	soup = makesoup(url).find_all('tr')
	unclean_pick4_list = []

	del unclean_pick4_list[0]

	for line in soup:
		unclean_pick4_list.append(line.text)

	clean_pick4_list = clean_data(unclean_pick4_list, game='pick4')

	if time == 'day':
		clean_pick4_list = day_or_evening(clean_pick4_list, time='day')
	elif time == 'evening':
		clean_pick4_list = day_or_evening(clean_pick4_list, time='evening')
	else:
		raise ValueError("Time must be either day or evening, got '{}'".format(
				time))

	del unclean_pick4_list
	return clean_pick4_list

def cash5(url):
	soup = makesoup(url).find_all('tr')
	unclean_cash5_list = []

	for line in soup:
		unclean_cash5_list.append(line.text)

	#The first element is table headings so we can delete it
	del unclean_cash5_list[0]

	clean_cash5_list = clean_data(unclean_cash5_list)
	
	del unclean_cash5_list
	return clean_cash5_list

def all_or_nothing(url):
	soup = makesoup(url).find_all('tr')
	unclean_aor_list = []

	for line in soup:
		unclean_aor_list.append(line.text)

	del unclean_aor_list[0]

	clean_aor_list = clean_data(unclean_aor_list, 'aor')

	del unclean_aor_list
	return clean_aor_list

def mega_millions(url):
	soup = makesoup(url).find_all('tr')
	unclean_mm_list = []

	for line in soup:
		unclean_mm_list.append(line.text)

	del unclean_mm_list[0]

	clean_mm_list = clean_data(unclean_mm_list, 'aor')

	del unclean_mm_list
	return clean_mm_list

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

if __name__ == '__main__':
	main()
