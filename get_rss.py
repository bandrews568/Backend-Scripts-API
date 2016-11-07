# Used to retrieve the most current lottery data via a rss feed
import re
from time import strptime
from datetime import datetime

import feedparser

class ParseRss(object):

    @staticmethod
    def format_data(summary, title):
        #(u'November 5 2016', u'0,2,1')
        numbers = summary.replace('-', ',')

        if "PB" or "MB" in numbers:
            numbers = re.sub('PB|PP|MB|MP', '', numbers)
            numbers = numbers.replace(' ', ',').replace(',,',',')

        if "," in title:
            raw_date = title.split(',')
            date_year = raw_date[2]
            # Change u' Nov' to a numerical number(note space before)
            date_month = strptime(raw_date[1][0:4].lstrip(),'%b').tm_mon
            date_day = re.findall(' \d.*$',raw_date[1])
            date_day = date_day[0].replace(' ','')
            if len(date_day) == 1:
                date_day = "0" + date_day[0]
                date_day = date_day.replace(' ','')
            date = date_year + '-' + str(date_month) + '-' + date_day
            date = date.replace(' ','')
        else:
            # Lucky For Life Winning Numbers on 10/31/2016
            raw_date = re.findall('\d\d/\d*./\d*.$', title)
            raw_date = raw_date[0]
            raw_date = datetime.strptime(raw_date, "%m/%d/%Y")
            date = raw_date.strftime('%Y-%m-%d')       
        return (date, numbers)


    def get_rss(self):
        """
            'title': u'Carolina Pick 3 Evening Winning Numbers', 
            'summary': u'4-4-8', 
        """
        url = 'http://www.nc-educationlottery.org/rss_winning_numbers.aspx'
        rss_data = feedparser.parse(url)

        for i in range(len(rss_data['entries'])):
            entry = rss_data['entries'][i]
            summary = entry['summary']
            title = entry['title']

            if "Carolina Pick 3 Daytime" in title:
                data = self.format_data(summary, title)
                pick3 = ["D", data[0], data[1]]

            elif "Carolina Pick 3 Evening" in title:
                """
                Date is in published instead of title
                'published': u'Monday, October 31, 2016'}
                """
                data = self.format_data(summary, entry['published'])
                pick3 = ["E", data[0], data[1]]
            
            elif "Carolina Pick 4 Daytime" in title:
                data = self.format_data(summary, title)
                pick4 = ["D", data[0], data[1]]

            elif "Carolina Pick 4 Evening" in title:
                data = self.format_data(summary, title)
                pick4 = ["D", data[0], data[1]]

            elif "Carolina Cash 5 Winning Numbers" in title:
                cash5 = self.format_data(summary, title)

            elif "Lucky For Life Winning Numbers" in title:
                lucky_for_life = self.format_data(summary, title)

            elif "Mega Millions Winning Numbers" in title:
                mega_millions = self.format_data(summary, title)

            elif "Powerball Winning Numbers" in title:
                powerball = self.format_data(summary, title)

if __name__ == '__main__':
    # TODO: Have to call all or nothing from here
    ParseRss().get_rss()
