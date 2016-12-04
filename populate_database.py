# Script used to populate the database tables
# For the most recent data we will use the information
# off the NC lottery RSS feed
import re
import time
import json
import urllib2
import logging
from datetime import datetime

from database_tools import DatabaseTools

import wget
from termcolor import colored
from bs4 import BeautifulSoup


logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.ERROR and logging.INFO)

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
        logger.error(color_error + "{} Response: {}".format(e.code, url))
        return
    except Exception as e:
        logger.error(color_error + "makesoup(): {}".format(e))
        return
    return soup

def format_date(date):
    """
        Change date to a format SQLite accepts.
        From: 'Thu, Nov 03, 2016'
        To: '2016/11/03'
    """
    try:
        og_date = datetime.strptime(date, "%a, %b %d, %Y")
        f_date = og_date.strftime('%Y-%m-%d')
        return f_date
    except Exception as e:
        logger.error(color_error + "format_date(): {}".format(e))


def pick3(url, time):
    try:
        logger.info(color_attempt + "Pick 3 '{}'".format(time))
        pick3_data = makesoup(url)
        get_date = pick3_data.find_all('td', {'class': 'date'})
        get_numbers = pick3_data.find_all('td', {'class': 'result'})
    except Exception as e:
        logger.error(color_error + "(Pick 3-{}): {}".format(time, e))
        return

    date_list = [format_date(line.text) for line in get_date]
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
        raise ValueError("Time must be either day or evening, got '{}'"
                         .format(time))

    for line in pick3_list: 
        DatabaseTools.insert_row('pick3', line)

    logger.info(color_success + "Pick 3 '{}'".format(time))
    # Returns data in a list of tuples in the following formats
    # ('D', u'2016/11/02, u'4,0,4')
    # ('E', u'2016/11/02', u'2,4,5')
    return pick3_list


def pick4(url, time):
    try:
        logger.info(color_attempt + "Pick 4 '{}'".format(time))
        pick4_data = makesoup(url)
        get_date = pick4_data.find_all('td', {'class': 'date'})
        get_numbers = pick4_data.find_all('td', {'class': 'result'})
    except Exception as e:
        logger.error(color_error + "(Pick 4-{}): {}".format(time, e))
        return

    date_list = [format_date(line.text) for line in get_date]
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
        raise ValueError("Time must be either day or evening, got '{}'"
                         .format(time))

    for line in pick4_list: 
        DatabaseTools.insert_row('pick4', line)

    logger.info(color_success + "Pick 4 '{}'".format(time))
    # Returns data in a list of tuples in the following formats
    # ('D', u'2016/11/02', u'0,5,1,0')
    # ('E', u'2016/11/02', u'9,2,6,6')
    return pick4_list


def cash5(url):
    try:
        logger.info(color_attempt + "Cash 5")
        cash5_data = makesoup(url)
        get_date = cash5_data.find_all('td', {'class': 'date'})
        get_numbers = cash5_data.find_all('td', {'class': 'result'})
        get_jackpot = cash5_data.find_all('td', {'class': 'jackpot'})
    except Exception as e:
        logger.error(color_error + "(Cash 5): {}".format(e))
        return

    date_list = [format_date(line.text) for line in get_date]
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

    for line in cash5_list: 
        DatabaseTools.insert_row('cash5', line)
    
    logger.info(color_success + "Cash 5")
    # Returns a list of tuples in this format:
    # (u'2016/11/02', u'2,24,29,33,38', u'$100,000')
    return cash5_list


def all_or_nothing(url, time):
    try:
        logger.info(color_attempt + "All or Nothing '{}'".format(time))
        aor_data = makesoup(url)
        get_date = aor_data.find_all('td', {'class': 'date'})
        get_numbers = aor_data.find_all('td', {'class': 'result'})
    except Exception as e:
        logger.error(color_error + "(All or Nothing-{}): {}".format(time, e))
        return

    date_list = [format_date(line.text) for line in get_date]
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
        raise ValueError("Time must be either day or evening, got '{}'"
                         .format(time))

    for line in aor_list: 
        DatabaseTools.insert_row('all_or_nothing', line)

    logger.info(color_success + "All or Nothing '{}'".format(time))
    # Returns a list of tuples in this format:
    # ('D', u'2016/11/02', u'1,3,6,9,11,12,14,15,16,19,20,22')
    return aor_list


def powerball():
    try:
        logger.info(color_attempt + "Powerball")
        filename = "powerball_{}.txt".format(time.strftime("%m-%d-%Y"))
        url = "http://www.powerball.com/powerball/winnums-text.txt"
        wget.download(url, out=filename)
    except Exception as e:
        logger.error(color_error + "(Powerball): {}".format(e))
        return

    # Make sure we are looking at the current data
    # Example filename: powerball_10-16-2016.txt
    if not filename[10:20] == time.strftime("%m-%d-%Y"):
        raise ValueError("'{}' is not current".format(filename))

    date_list = []
    number_list = []

    try:
        # Data structures:
        # Note: double spaces between all the powerball #'s
        # Without multiplier
        # 06/21/2000  43  01  28  27  24  25 \r\n
        # With
        # 04/19/2006  32  53  34  05  28  10  4 \r\n
        with open(filename, "r") as f:
            for line in f:
                try:
                    date_data = line[0:10]
                    date = datetime.strptime(date_data, "%m/%d/%Y")
                    date = date.strftime('%Y-%m-%d')
                except Exception as e:
                    logger.error(color_error + "(Powerball): {}".format(e))
                    logger.error(color_error + "(Powerball): {}".format(line))
                    continue
                raw_number_data = line[11:].strip().split("  ")
                number_data = ','.join(raw_number_data)
                date_list.append(date)
                number_list.append(number_data)
    except IOError:
        logger.error(color_error + "opening: {}".format(filename))
        return

    powerball_list = zip(date_list, number_list)
    # Deleting: ('Draw Date ', ['WB1 WB2 WB3 WB4 WB5 PB', 'PP'])
    del powerball_list[0]

    for line in powerball_list: 
        DatabaseTools.insert_row('powerball', line)

    logger.info(color_success + "Powerball")
    # Returns a list of tuples in this format:
    # ('2016/11/02', '18,54,61,13,37,05,2')
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
    url = 'https://data.ny.gov/resource/h6w8-42p9.json'

    try:
        logger.info(color_attempt + "Mega Millions")
        open_page = urllib2.urlopen(url)
        json_data = json.loads(open_page.read())
    except urllib2.HTTPError as e:
        logger.error(color_error + "{} Response: {}".format(e.code, url))
        return
    except Exception as e:
        logger.error(color_error + "(Mega Millions): {}".format(e))

    mm_list = []

    for line in json_data:
        date = line['draw_date']
        # Take out the time: 2007-05-11T00:00:00.000
        date = re.sub('T\d\d:\d\d:00\.000', '', date)
        try:
            numbers = line['winning_numbers'] + ' ' + line['mega_ball'] + \
                      ' ' + line['multiplier']
        except KeyError:
            # line['multiplier'] isn't in older results
            numbers = line['winning_numbers'] + ' ' + line['mega_ball']
        mm_list.append((date, numbers))

    for line in mm_list: 
        DatabaseTools.insert_row('mega_millions', line)

    logger.info(color_success + "Mega Millions")
    # Returns a list of tuples in this format:
    # (u'2016-11-01', u'19 24 31 39 45 13 02')
    return mm_list


def lucky_4_life(url):
    try:
        logger.info(color_attempt + "Lucky For Life")
        lucky_data = makesoup(url)
        get_date = lucky_data.find_all('td', {'class': 'date'})
        get_numbers = lucky_data.find_all('td', {'class': 'result'})
    except Exception as e:
        logger.error(color_error + "(Lucky For Life): {}".format(e))
        return

    date_list = [format_date(line.text) for line in get_date]
    number_list = []

    for line in get_numbers:
        # This is the data structure:
        # '\n6\n23\n33\n44\n45\n9  Lucky Ball\n'
        line = re.sub('\n', ' ', line.text)
        # This is what we're working with now:
        # ' 24 28 30 33 34 18  Lucky Ball '
        line = re.sub('Lucky Ball', '', line).strip()
        # Put commas between the numbers
        line = re.sub(' ', ',', line)
        number_list.append(line)

    lucky_list = zip(date_list, number_list)

    for line in lucky_list: 
        DatabaseTools.insert_row('lucky_for_life', line)

    logger.info(color_success + "Lucky For Life")
    # Returns a list of tuples in this format:
    # (u'2016-11-01', u'3,4,12,32,45,5')
    return lucky_list


def main():
    games = {
        'pick3_day': 'http://www.lotteryusa.com/north-carolina/midday-3/year',
        'pick3_evening': 'http://www.lotteryusa.com/north-carolina/pick-3/year',
        'pick4_day': 'http://www.lotteryusa.com/north-carolina/midday-pick-4/year',
        'pick4_evening': 'http://www.lotteryusa.com/north-carolina/pick-4/year',
        'cash5': 'http://www.lotteryusa.com/north-carolina/cash-5/year',
        'aor_day': 'http://www.lotteryusa.com/north-carolina/midday-all-or-nothing/year',
        'aor_evening': 'http://www.lotteryusa.com/north-carolina/night-all-or-nothing/year',
        'lucky_4_life': 'http://www.lotteryusa.com/north-carolina/lucky-4-life/year'
    }

    pick3(games['pick3_day'], 'day')
    pick3(games['pick3_evening'], 'evening')
    pick4(games['pick4_day'], 'day')
    pick4(games['pick4_evening'], 'evening')
    cash5(games['cash5'])
    all_or_nothing(games['aor_day'], 'day')
    all_or_nothing(games['aor_evening'], 'evening')
    powerball()
    mega_millions()
    lucky_4_life(games['lucky_4_life'])


if __name__ == '__main__':
    main()
