'''
This is tiny experimental project focus on scraping data of fellows exhibited
in the Insight Data Science website. It aims to identiy if there are connections
among academic research, insight projects, and hiring companies.
'''

from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from itertools import chain
import seaborn as sns
import pandas as pd

class InsightFellows(object):

    def __init__(self, df, link, categories, n_pages=8):
        self.df = df
        self.link = link
        self.categories = categories
        self.n_pages = n_pages
        self.scrape_info()

    def scrape_info(self):
        print('Scraping data from Insight website ...')
        for j in range(len(self.categories)):
            name = self.categories[j]
            class_ = re.compile("tooltip_{0}".format(name))
            lists = []
            for i in range(1, self.n_pages+1):
                url = self.link + str(i)
                uh = urlopen(url)
                soup = BeautifulSoup(uh, 'html.parser')
                soup = soup.find_all('div', class_=class_)
                item_list = [info.text for info in soup]
                lists.append(item_list)
            items = [item for item in chain(*lists)]
            df_series = pd.Series(items, name=name)
            self.df = pd.concat([self.df, df_series], axis=1)
        return self.df

    def search_companies(self, company):
        print('Searching the requested companies in the dataset ...')
        return self.df[self.df['company'] == company]

def main():
    print('Please input your desired company name: ')
    company = input()
    link = 'https://www.insightdatascience.com/fellows?e9e38a35_page='
    categories = ['name', 'background', 'project', 'company']
    df = pd.DataFrame()
    data_fellow = InsightFellows(df, link, categories)
    print(data_fellow.search_companies(company))

if __name__ == '__main__':
    main()
