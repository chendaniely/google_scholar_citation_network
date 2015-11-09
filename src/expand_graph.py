import pandas as pd
import requests
from random import randint, random
from time import sleep

from bs4 import BeautifulSoup

import scholar
import scrape


class GoogleScholarArticleSimple(scrape.CitationResults):
    def __init__(self):
        self.citation_url_generic = 'https://scholar.google.com/scholar?start={}&hl=en&as_sdt=2005&sciodt=0,5&cites={}&scipsc='
        self.cluster_id = None

    def set_search_soup(self, first_page=0):
        search_page_url = current_article.citation_url_generic.format(first_page, self.cluster_id)
        r = requests.get(search_page_url)
        self.soup = BeautifulSoup(r.text)
        return(self)


def main():
    data = pd.DataFrame()

    f = open('../results/5556531000720111691.csv.bkup', 'r')
    for idx, line in enumerate(f):
        data_values = line.split(',', 2)
        to_append = pd.DataFrame([data_values])
        data = data.append(to_append)
    f.close()

    #
    # for each cluster id
    #
    for from_cluster_id in range(data.shape[0])[:1]: # just get the first one, for now\
        print(from_cluster_id)
        cluster_id = data.iloc[from_cluster_id, 0]
        try:
            cluster_id = int(cluster_id)
        except ValueError:
            continue

        querier = scholar.ScholarQuerier()
        settings = scholar.ScholarSettings()
        query = scholar.SearchScholarQuery()
        query_cluster = scholar.ClusterScholarQuery(cluster=cluster_id)
        querier.send_query(query_cluster)

        #
        # for each article in search results
        #
        for article in querier.articles[:1]: # get first article result, for now
            article.attrs.get('url_citations')[0]
            current_article = GoogleScholarArticleSimple()
            current_article.cluster_id = cluster_id
            current_article.set_search_soup().set_num_search_results().set_num_search_pages()

            # gs_r = current_article.soup.find_all("div", class_="gs_r")

            #
            # for each search page result of citing article
            #
            for page_idx, search_page_number in enumerate(range(current.article.num_search_pages)[:1]): # get first page result for now
                url = citations_url_generic.format(search_page_number * 10, from_cluster_id)
                r = requests.get(url)
                soup = BeautifulSoup(r.text)
                gs_r = soup.find_all("div", class_="gs_r")
                # print(len(gs_r))

                output_file_path = '../results/01-{}.csv'.format(from_cluster_id)

                f = open(output_file_path, 'w')
                f.close()

                #
                # for each search result
                #
                for citing_article_soup in gs_r:
                    result_article = DanGoogleScholarArticle(soup=citing_article_soup)
                    result_article.parse_title()
                    # print(result_article.title)
                    result_article.parse_cluster_id()
                    # seed_cluster_id = result_article.cluster_id
                    # print(seed_cluster_id)
                    f = open(output_file_path, 'a+')
                    str_to_write = '{}\t|\t{}\t|\t{}\n'.\
                                   format(result_article.cluster_id,
                                          cluster_id,
                                          citing_article_soup)
                    f.write(str_to_write)
                    f.close()
                    sleep_time = random() * randint(10, 100)
                    print('cluster_id: {}, page: {}, sleeping: {}'.format(from_cluster_id, page_number, sleep_time))
                    sleep(sleep_time)


if __name__ == '__main__':
    main()
