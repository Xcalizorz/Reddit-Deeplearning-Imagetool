# -*- coding: utf-8 -*-
"""Helper functions to interact with our specific DB

"""


def insert_reddit_data_to_db(reddit_db_handler, reddit_data):
    """Allows easier insertion into our specific database

    :param reddit_db_handler:
        A RedditChecker.db_handler object
    :type reddit_db_handler: DBHandler
    :param post_data: Reddit data, taken from RedditChecker()
    """
    for post in reddit_data:
        for table_name, post_data in post.items():
            reddit_db_handler.insert_to_db(table_name, post_data)
