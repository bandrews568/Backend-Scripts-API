# Script used to populate the database tables
# For the most recent data we will use the information
# off the NC lottery RSS feed
import re
import time
import json
import urllib2

import wget
from termcolor import colored
from bs4 import BeautifulSoup

color_attempt = colored('[Attempt] ', 'yellow')
color_error = colored('[Error] ', 'red')
color_success = colored('[Success] ', 'green')

def makesoup(url):
    """
        Request the page and parse the infromation
           to return a soup object.
    """
    try:
        req = urllib2.Request(url)
        page = urllib2.urlopen(req)
        soup = BeautifulSoup(page.read(), 'html.parser')
    except urllib2.HTTPError as e:
        print color_error + "{} Response: {}".format(e.code, url)
        return
    except Exception as e:
        print color_error + "makesoup(): {}".format(e)
        return
    return soup


def pick3(url, time):
    try:
        print color_attempt + "Pick 3 '{}'".format(time)
        get_date = makesoup(url).find_all('td', {'class': 'date'})
        get_numbers = makesoup(url).find_all('td', {'class': 'result'})
    except Exception as e:
        print color_error + "(Pick 3-{}): {}".format(time, e)
        return

    date_list = [line.text for line in get_date]
    number_list = []

    for line in get_numbers:
        # This is the data structure: u'\n6\n6\n0\n0\n\n'
        line = re.sub('\n', ',', line.text[1:], 2)
        # This is what we're working with now:
        # u'\n2,6,14,31,38\n\n'
        line = re.sub('\n', '', line)
        number_list.append(line)

    if time == 'day':
        pick3_list = zip("D" * len(date_list), date_list, number_list)
    elif time == 'evening':
        pick3_list = zip("E" * len(date_list), date_list, number_list)
    else:
        raise ValueError("Time must be either day or evening, got '{}'" \
                         .format(time))

    print color_success + "Pick 3 '{}'".format(time)
    return pick3_list


def pick4(url, time):
    try:
        print color_attempt + "Pick 4 '{}'".format(time)
        get_date = makesoup(url).find_all('td', {'class': 'date'})
        get_numbers = makesoup(url).find_all('td', {'class': 'result'})
    except Exception as e:
        print color_error + "(Pick 4-{}): {}".format(time, e)
        return

    date_list = [line.text for line in get_date]
    number_list = []

    for line in get_numbers:
        # This is the data structure: u'\n6\n6\n0\n0\n\n'
        line = re.sub('\n', ',', line.text[1:], 3)
        # This is what we're working with now:
        # u'\n2,6,14,31,38\n\n'
        line = re.sub('\n', '', line)
        number_list.append(line)

    if time == 'day':
        pick4_list = zip("D" * len(date_list), date_list, number_list)
    elif time == 'evening':
        pick4_list = zip("E" * len(date_list), date_list, number_list)
    else:
        raise ValueError("Time must be either day or evening, got '{}'" \
                         .format(time))

    print color_success + "Pick 4 '{}'".format(time)
    return pick4_list


def cash5(url):
    try:
        print color_attempt + "Cash 5"
        get_date = makesoup(url).find_all('td', {'class': 'date'})
        get_numbers = makesoup(url).find_all('td', {'class': 'result'})
        get_jackpot = makesoup(url).find_all('td', {'class': 'jackpot'})
    except Exception as e:
        print color_error + "(Cash 5): {}".format(e)
        return

    date_list = [line.text for line in get_date]
    jackpot_list = [line.text for line in get_jackpot]
    number_list = []

    for line in get_numbers:
        # This is the data structure: u'\n2\n6\n14\n31\n38\n\n'
        line = re.sub('\n', ',', line.text[1:], 4)
        # This is what we're working with now:
        # u'/n2,6,14,31,38\n\n'
        line = re.sub('\n', '', line)
        number_list.append(line)

    cash5_list = zip(date_list, number_list, jackpot_list)
    # (u'Thu, Oct 22, 2015', u'7,21,24,27,30', u'$60,000')
    print color_success + "Cash 5"
    return cash5_list


def all_or_nothing(url, time):
    try:
        print color_attempt + "All or Nothing '{}'".format(time)
        get_date = makesoup(url).find_all('td', {'class': 'date'})
        get_numbers = makesoup(url).find_all('td', {'class': 'result'})
    except Exception as e:
        print color_error + "(All or Nothing-{}): {}".format(time, e)
        return

    date_list = [line.text for line in get_date]
    number_list = []

    for line in get_numbers:
        # This is the data structure:
        # u'\n3\n4\n6\n7\n9\n10\n11\n15\n17\n20\n23\n24\n\n'
        line = re.sub('\n', ',', line.text[1:], 11)
        # This is what we're working with now:
        # u'\n3,6,7,9,10,11,15,17,20,23,24\n\n'
        line = re.sub('\n', '', line)
        number_list.append(line)

    if time == 'day':
        aor_list = zip("D" * len(date_list), date_list, number_list)
    elif time == 'evening':
        aor_list = zip("E" * len(date_list), date_list, number_list)
    else:
        raise ValueError("Time must be either day or evening, got '{}'" \
                         .format(time))

    print color_success + "All or Nothing '{}'".format(time)
    return aor_list


def powerball():
    try:
        print color_attempt + "Powerball"
        filename = "powerball_{}.txt".format(time.strftime("%m-%d-%Y"))
        url = "http://www.powerball.com/powerball/winnums-text.txt"
        print wget.download(url, out=filename)
    except Exception as e:
        print color_error + "(Powerball): {}".format(e)
        return

    # Make sure we are looking at the current data
    # Example filename: powerball_10-16-2016.txt
    if filename[10:20] == time.strftime("%m-%d-%Y"):
        pass
    else:
        raise ValueError("'{}' is not current".format(filename))

    date_list = []
    number_list = []

    try:
        # Data structures:
        # Note: double spaces between all the powerball #'s
        # Without multipler
        # 06/21/2000  43  01  28  27  24  25 \r\n
        # With
        # 04/19/2006  32  53  34  05  28  10  4 \r\n
        with open(filename, "r") as f:
            for line in f:
                date_data = line[0:10]
                number_data = line[11:]
                number_data = number_data.lstrip().rstrip()
                number_data = number_data.split("  ")
                date_list.append(date_data)
                number_list.append(number_data)
    except IOError:
        print color_error + "opening: {}".format(filename)

    powerball_list = zip(date_list, number_list)

    print color_success + "Powerball"
    return powerball_list


def mega_millions():
    """
        Data structure(JSON):
        {
        "draw_date": "2016-10-21T00:00:00.000",
        "mega_ball": "03",
        "multiplier": "04",
        "winning_numbers": "12 43 44 48 66"
        }
    """
    try:
        print color_attempt + "Mega Millions"
        url = 'https://data.ny.gov/resource/h6w8-42p9.json'
        open_page = urllib2.urlopen(url)
        json_data = json.loads(open_page.read())
    except urllib2.HTTPError as e:
        print color_error + "{} Response: {}".format(e.code, url)
        return
    except Exception as e:
        print color_error + "(Mega Millions): {}".format(e)

    data_list = []

    for line in json_data:
        data_list.append(line)
    print color_success + "Mega Millions"
    return data_list


def lucky_4_life(url):
    try:
        print color_attempt + "Lucky For Life"
        get_date = makesoup(url).find_all('td', {'class': 'date'})
        get_numbers = makesoup(url).find_all('td', {'class': 'result'})
    except Exception as e:
        print color_error + "(Lucky For Life): {}".format(e)
        return

    number_list = []
    date_list = [line.text for line in get_date]

    for line in get_numbers:
        # This is the data structure:
        # '\n6\n23\n33\n44\n45\n9  Lucky Ball\n'
        line = re.sub('\n', ' ', line.text)
        # This is what we're working with now:
        # 24 28 30 33 34 18  Lucky Ball
        line = re.sub('Lucky Ball', '', line)
        # ' 24 28 30 33 34 18 '
        line = line.lstrip().rstrip()
        # Put commas between the numbers
        line = re.sub(' ', ',', line)
        number_list.append(line)

    lucky_list = zip(date_list, number_list)

    print color_success + "Lucky For Life"
    return lucky_list


def main():
    games = {
        'pick3_mid_day': 'http://www.lotteryusa.com/north-carolina/midday-3/year',
        'pick3_evening': 'http://www.lotteryusa.com/north-carolina/pick-3/year',
        'pick4_mid_day': 'http://www.lotteryusa.com/north-carolina/midday-pick-4/year',
        'pick4_evening': 'http://www.lotteryusa.com/north-carolina/pick-4/year',
        'cash5': 'http://www.lotteryusa.com/north-carolina/cash-5/year',
        'aor_mid_day': 'http://www.lotteryusa.com/north-carolina/midday-all-or-nothing/year',
        'aor_evening': 'http://www.lotteryusa.com/north-carolina/night-all-or-nothing/year',
        'lucky_4_life': 'http://www.lotteryusa.com/north-carolina/lucky-4-life/year'
    }

    pick3(games.get('pick3_mid_day'), 'day')
    pick3(games.get('pick3_evening'), 'evening')
    pick4(games.get('pick4_mid_day'), 'day')
    pick4(games.get('pick4_evening'), 'evening')
    cash5(games.get('cash5'))
    all_or_nothing(games.get('aor_mid_day'), 'day')
    all_or_nothing(games.get('aor_evening'), 'evening')
    powerball()
    mega_millions()
    lucky_4_life(games.get('lucky_4_life'))


if __name__ == '__main__':
    main()
