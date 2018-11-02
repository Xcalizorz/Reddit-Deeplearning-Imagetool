# -*- coding: utf-8 -*-
"""Helper functions to interact with our specific DB

"""
import re

import requests


def generate_reddit_data(reddit, reddit_sorts, reddit_times):
    """Helper to generate all needed data

    :param reddit: The RedditChecker object
    :type reddit: RedditChecker
    :param reddit_sorts: The sort arguments given by the user
    :type reddit_sorts: str
    :param reddit_times: The time arguments given by the user
    :type reddit_times: str
    """
    reddit_sorts = reddit_sorts.split(" ")
    reddit_times = reddit_times.split(" ")

    for reddit_sort in reddit_sorts:
        for reddit_time in reddit_times:
            yield reddit.subreddit_data(reddit_sort=reddit_sort, reddit_time=reddit_time)


def insert_reddit_data_to_db(reddit_db_handler, data):
    """Allows easier insertion into our specific database

    :param reddit_db_handler:
        A RedditChecker.db_handler object
    :type reddit_db_handler: DBHandler
    :param data: Reddit data, taken from RedditChecker()
    """
    for reddit_data in data:
        for post in reddit_data:
            for table_name, post_data in post.items():
                reddit_db_handler.insert_to_db(table_name, post_data)


# Seperate in the future
USER_AGENT = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Content-Type': 'application/json',
}


def google_reverse_image_search(image_url):
    """Uses googles reverse image search
    Returns main information as a dictionary

    :param image_url:
        A URL to the image to be analyzed
    :return: 
        - Google Permalink to the search
        - Guess whats on the picture
        - Link of first result
    :rtype: Dict
    """
    google_knows = False
    google_url = f'https://images.google.com/searchbyimage?image_url={image_url}'
    response = requests.get(google_url, headers=USER_AGENT)

    result = {
        'google_permalink': None,
        'guess': None,
        'first_result': None,
    }

    if response.status_code == 503:
        if not google_knows:
            print("Google found out you're a bot!\nAuthorize here:\t")
            print(response.url)
            google_knows = True
        return result

    try:
        information = re.search(r'<a class="fKDtNb" href="(.*?)</a>',
                                response.text).group(1).split('style="font-style:italic">')
        result['google_permalink'] = information[0]
        result['guess'] = information[1].title()
    except AttributeError:
        pass

    try:
        result['first_result'] = re.search(r'<div class="r"><a href="(.*?)"', response.text).group(1)
    except AttributeError:
        pass

    return result
