# Used to retrieve the most current lottery data via a rss feed
import re
from time import strptime
from datetime import datetime
from database_tools import DatabaseTools

import feedparser


class ParseRss:

    @staticmethod
    def format_data(summary, title):
        trim_spaces = lambda x: x.replace(' ', '')
        #(u'November 5 2016', u'0-2-1')
        numbers = summary.replace('-', ',')

        if 'PB' or 'MB' in numbers:
            numbers = re.sub('PB|PP|MB|MP', '', numbers)
            numbers = trim_spaces(numbers).replace(',,',',')

        if ',' in title:
            raw_date = title.split(',')
            date_year = raw_date[2]
            # Change u' Nov' to a numerical number(note space before)
            date_month = strptime(raw_date[1][0:4].lstrip(),'%b').tm_mon
            date_day = re.findall(' \d.*$',raw_date[1])
            date_day = trim_spaces(date_day[0])
            if len(date_day) == 1:
                date_day = '0' + date_day[0]
                date_day = trim_spaces(date_day)
            date = date_year + '-' + str(date_month) + '-' + date_day
            date = trim_spaces(date)
        else:
            # Lucky For Life Winning Numbers on 10/31/2016
            raw_date = re.findall('\d\d/\d*./\d*.$', title)
            raw_date = raw_date[0]
            raw_date = datetime.strptime(raw_date, '%m/%d/%Y')
            date = raw_date.strftime('%Y-%m-%d')       
        return (date, numbers)


    def get_rss(self):
        """
            'title': u'Carolina Pick 3 Evening Winning Numbers', 
            'summary': u'4-4-8', 
        """
        url = 'http://www.nc-educationlottery.org/rss_winning_numbers.aspx'
        rss_data = feedparser.parse(url)
        add_row = lambda x, y: DatabaseTools.insert_row(x, y)

        for i in range(len(rss_data['entries'])):
            entry = rss_data['entries'][i]
            summary = entry['summary']
            title = entry['title']

            if 'Carolina Pick 3 Daytime' in title:
                data = self.format_data(summary, title)
                pick3 = ["D", data[0], data[1]]
                add_row("pick3", pick3)

            elif 'Carolina Pick 3 Evening' in title:
                """
                Date is in published instead of title
                'published': u'Monday, October 31, 2016'}
                """
                data = self.format_data(summary, entry['published'])
                pick3 = ["E", data[0], data[1]]
                add_row('pick3', pick3)
            
            elif 'Carolina Pick 4 Daytime' in title:
                data = self.format_data(summary, title)
                pick4 = ['D', data[0], data[1]]
                add_row('pick4', pick4)

            elif 'Carolina Pick 4 Evening' in title:
                data = self.format_data(summary, title)
                pick4 = ['D', data[0], data[1]]
                add_row('pick4', pick4)

            elif 'Carolina Cash 5 Winning Numbers' in title:
                cash5 = self.format_data(summary, title)
                add_row('cash5', cash5)

            elif 'Lucky For Life Winning Numbers' in title:
                lucky_for_life = self.format_data(summary, title)
                add_row('lucky_4_life', lucky_4_life)

            elif 'Mega Millions Winning Numbers' in title:
                mega_millions = self.format_data(summary, title)
                add_row('mega_millions', mega_millions)

            elif 'Powerball Winning Numbers' in title:
                powerball = self.format_data(summary, title)
                add_row('powerball', powerball)

if __name__ == '__main__':
    from populate_database import all_or_nothing   
    aor_d = 'http://www.lotteryusa.com/north-carolina/midday-all-or-nothing/year'
    aor_e = 'http://www.lotteryusa.com/north-carolina/night-all-or-nothing/year'
    aor_day = all_or_nothing(aor_d, 'day')
    aor_evening = all_or_nothing(aor_e, 'evening')
    for x in aor_day: 
        DatabaseTools.insert_row('all_or_nothing', x)
    for x in aor_evening: 
        DatabaseTools.insert_row('all_or_nothing', x)
    ParseRss().get_rss()
