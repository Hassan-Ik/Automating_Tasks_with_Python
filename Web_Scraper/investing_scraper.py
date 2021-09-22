# Accessing OS path
import os
# Web Scraping
from bs4 import BeautifulSoup
# Sending Http Request
import requests
import numpy as np

import datetime
# For Saving the scraped data in csv file
import pandas as pd
# For passing arguments to file in cmd
import argparse


def main(url, name, news_headline_tag, news_headline_class, article_time_tag, article_content_class):
    r1 = requests.get(url)
    coverpage = r1.content
    soup1 = BeautifulSoup(coverpage, 'html5lib')

    #     coverpage_news_headline = soup1.find_all('h3', class_='fxs_entryHeadline')
    coverpage_news_headline = soup1.find_all(news_headline_tag, class_=news_headline_class)

    # Scraping the first 3 articles
    number_of_articles = 3
    # Empty lists for content, links and titles
    news_contents = []
    list_links = []
    list_titles = []
    list_date = []

    for n in np.arange(0, number_of_articles):


        # Getting the link of the article
        link = coverpage_news_headline[n].find('a')['href']
        list_links.append(link)

        # Getting the title
        title = coverpage_news_headline[n].find('a').get_text()
        list_titles.append(title)

        # Reading the content (it is divided in paragraphs)
        article = requests.get(link)
        article_content = article.content
        soup_article = BeautifulSoup(article_content, 'html5lib')
        #         date = soup_article.find('time').get_text()
        date = soup_article.find(article_time_tag).get_text()
        list_date.append(date.split(' ')[0])
        #         body = soup_article.find_all('div', class_='fxs_article_content')
        body = soup_article.find_all('div', class_=article_content_class)

        x = body[0].find_all('p')

        # Unifying the paragraphs
        list_paragraphs = []
        for p in np.arange(0, len(x)):
            paragraph = x[p].get_text()
            list_paragraphs.append(paragraph)
            final_article = " ".join(list_paragraphs)

        news_contents.append(final_article)

    df = pd.DataFrame()
    df["Publish_date"] = list_date
    df["News_Title"] = list_titles
    df["News_Content"] = news_contents

    filepath = './textual_data/{0}.csv'.format(name)
    if os.path.isfile(filepath):
        existing_file = pd.read_csv(filepath)
        new_df = pd.merge(existing_file, df,
                          how='outer')
        new_df.to_csv('./textual_data/{0}.csv'.format(name), index=False)
    else:
        df.to_csv('./textual_data/{0}.csv'.format(name), index=False)
    return "Successful"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--url', type=str, default='https://www.fxstreet.com/currencies/eurusd', help="Enter The Url",
                        required=True)
    parser.add_argument('--name', type=str, help='Enter CSV file path and name', required=True)
    parser.add_argument('--headline_tag', type=str, default='h3', help='Enter News Article Headline Text Tag',
                        required=True)
    parser.add_argument('--headline_class', type=str, help="Enter The Headline Article Class Name", required=True)
    parser.add_argument('--article_time', type=str, default='time', help='Enter The Article Published Time Tag',
                        required=True)
    parser.add_argument('--article_content', type=str, help="Enter The Article Paragraph div tag Class Name",
                        required=True)
    args = parser.parse_args()
    print(args.name)
    print(args.url)
    main(args.url, args.name, args.headline_tag, args.headline_class, args.article_time, args.article_content)
