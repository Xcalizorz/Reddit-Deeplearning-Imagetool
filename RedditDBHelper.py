# -*- coding: utf-8 -*-
"""Helper functions to interact with our specific DB

"""


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
