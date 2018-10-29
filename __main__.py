# -*- coding: utf-8 -*-
from FileReader import FileReader
from RedditChecker import RedditChecker
from RedditDBHelper import *


def main():
    reddit = RedditChecker('memes something funny earthporn spaceporn')

    reddit_data = reddit.subreddit_data(reddit_sort='top', reddit_time='month')

    sql_create_commands = FileReader.read_file('./sql/create.sql')

    #########################################################
    # Uncomment, if you want to re-/create the db
    # reddit.db_handler.create_db
    # reddit.db_handler.init_database(sql_create_commands)
    #########################################################

    insert_reddit_data_to_db(reddit.db_handler, reddit_data)

if __name__ == '__main__':
    main()
