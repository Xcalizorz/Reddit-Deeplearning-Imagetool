# -*- coding: utf-8 -*-
from FileReader import FileReader
from RedditChecker import RedditChecker
from RedditDBFormatter import RedditDBFormatter
from RedditDBHelper import *


def main():
    reddit = RedditChecker('memes something funny')
    reddit_formatter = RedditDBFormatter()

    reddit_data = reddit_formatter.format_data(
        reddit.subreddit_data(reddit_sort='controversial', reddit_time='year')
    )

    sql_create_commands = FileReader.read_file('./sql/create.sql')

    # Uncomment, if you want to re-/create the db
    reddit.db_handler.create_db
    reddit.db_handler.init_database(sql_create_commands)

    insert_reddit_data_to_db(reddit.db_handler, reddit_data)

if __name__ == '__main__':
    main()
