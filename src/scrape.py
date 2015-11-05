
# coding: utf-8

# In[ ]:

import re
from random import randint, random
from time import sleep
import warnings

import networkx as nx
from bs4 import BeautifulSoup
import requests

import scholar


# In[ ]:

class CitationResults(object):
    def __init__(self, **kwargs):
        self.soup = kwargs.get('soup')
        self.num_search_pages = None
    def set_num_search_results(self):
        str_num_results = self.soup.find_all('div', id='gs_ab_md')[0].get_text().split()[1]
        self.num_results = int(str_num_results.replace(',', ''))
        return(self)
    def set_num_search_pages(self):
        # floor division
        self.num_search_pages = self.num_results // 10
        return(self)
    def parse_current_page(self):
        gs_r = soup.find_all("div", class_="gs_r")


#             'title':         [None, 'Title',          0],
#             'url':           [None, 'URL',            1],
#             'year':          [None, 'Year',           2],
#             'num_citations': [0,    'Citations',      3],
#             'num_versions':  [0,    'Versions',       4],
#             'cluster_id':    [None, 'Cluster ID',     5],
#             'url_pdf':       [None, 'PDF link',       6],
#             'url_citations': [None, 'Citations list', 7],
#             'url_versions':  [None, 'Versions list',  8],
#             'url_citation':  [None, 'Citation link',  9],
#             'excerpt':       [None, 'Excerpt',       10],

# In[ ]:

class DanGoogleScholarArticle(object):
    def __init__(self, **kwargs):
        self.soup = kwargs.get('soup')
        self._title = None
        self._url = None
        self.year = None
        self.num_citations = None
        self.num_vertions = None
        self.cluster_id = None
        self.url_pdf = None
        self.url_citations = None
        self.url_versions = None
        self.url_citation = None
        self.excerpt = None

    def parse_all(self):
        self.parse_title()
        return(self)

    def parse_title(self):
        soup_title = self.soup.find('h3', class_='gs_rt')
        title = soup_title.find('a').get_text()
        self.title = title
        return(self)

    def parse_cluster_id(self, cluster_str_index=0, cluster_id_str_index=0):
        #print('*' * 80)
        #print('Below is self.soup')
        #print(self.soup)

        #print('*' * 80)
        #print('Below is the soup cluster id')
        soup_cluster_id = self.soup.find_all('div', class_='gs_fl')[-1]
        #print(soup_cluster_id)

        #print('*' * 80)
        #print('Below is the cluster id link')
        cluster_id_link = soup_cluster_id.find('a', class_='gs_nph').get('href')
        #print(cluster_id_link)

        pattern_cluster = re.compile('cluster=\d+')
        cluster_str = pattern_cluster.findall(cluster_id_link)[cluster_str_index]

        pattern_cluster_id = re.compile('\d+')
        cluster_id_str = pattern_cluster_id.findall(cluster_str)[cluster_id_str_index]
        self.cluster_id = int(cluster_id_str)
        return(self)

    @property
    def title(self):
        return self._title
    @title.setter
    def title(self, value):
        self._title = value

    @property
    def url(self):
        return self._url
    @url.setter
    def url(self, value):
        self._url = value


# In[ ]:

scholar_article = scholar.ScholarArticle()
scholar_article_parser = scholar.ScholarArticleParser()


# In[ ]:

querier = scholar.ScholarQuerier()
settings = scholar.ScholarSettings()
query = scholar.SearchScholarQuery()


# In[ ]:

query.set_author('eagly')


# In[ ]:

query.set_words('psychology of attitudes')


# In[ ]:

querier.send_query(query)


# In[ ]:

querier.articles[0].as_txt()


# In[ ]:

querier.articles[0].attrs


# In[ ]:

SEED_ARTICLE = querier.articles[0]
assert(SEED_ARTICLE.attrs.get('title')[0] == 'The psychology of attitudes.')


# In[ ]:

type(SEED_ARTICLE)


# In[ ]:

SEED_ARTICLE.attrs['cluster_id'][0]


# In[ ]:

citations_url = SEED_ARTICLE.attrs.get('url_citations')[0]


# In[ ]:

citations_url


# In[ ]:

citations_url_generic = 'https://scholar.google.com/scholar?start={}&hl=en&as_sdt=2005&sciodt=0,5&cites=5556531000720111691&scipsc='
citations_url_generic


# In[ ]:

citations_url_generic.format('0')


# In[ ]:

r = requests.get(citations_url_generic.format('0'))


# In[ ]:

soup = BeautifulSoup(r.text)


# In[ ]:

citation_results = CitationResults(soup=soup)
citation_results.set_num_search_results().set_num_search_pages()
citation_results.num_results


# In[ ]:

num_search_pages = citation_results.num_search_pages
num_search_pages


# In[ ]:

gs_r = soup.find_all("div", class_="gs_r")


# In[ ]:

len(gs_r)


# In[ ]:

citing_article_soup = gs_r[2]


# In[ ]:

result_article = DanGoogleScholarArticle(soup=citing_article_soup)


# In[ ]:

result_article.parse_title()
result_article.title


# In[ ]:

result_article.parse_cluster_id()


# In[ ]:

SEED_CLUSTER_ID = result_article.cluster_id
SEED_CLUSTER_ID


# In[ ]:

with open('../results/{}.csv'.format(SEED_ARTICLE.attrs['cluster_id'][0]), 'w+') as f:
    for page_url, page_number in enumerate(range(num_search_pages)):
        r = requests.get(citations_url_generic.format(page_url * 10))
        soup = BeautifulSoup(r.text)
        citations_url_generic.format('0')
        gs_r = soup.find_all("div", class_="gs_r")
        # print(len(gs_r))
        for citing_article_soup in gs_r:
            result_article = DanGoogleScholarArticle(soup=citing_article_soup)
            result_article.parse_title()
            # print(result_article.title)
            result_article.parse_cluster_id()
            seed_cluster_id = result_article.cluster_id
            # print(seed_cluster_id)
            str_to_write = '{}),{}\n'.format(result_article.cluster_id, SEED_CLUSTER_ID)
            f.write(str_to_write)
        sleep_time = random() * randint(10, 50)
        print('page: {}, sleeping: {}'.format(page_number, sleep_time))
        sleep(sleep_time)


# In[ ]:
