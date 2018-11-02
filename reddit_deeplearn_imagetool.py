# -*- coding: utf-8 -*-
import json
import re

import requests

from cmd_line_args import arg_parse_info
from FileReader import FileReader
from RedditChecker import RedditChecker
from RedditDBHelper import *

USER_AGENT = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Content-Type': 'application/json',
}


def fetch_results(image_url):
    google_url = f'https://images.google.com/searchbyimage?image_url={image_url}'
    response = requests.get(google_url, headers=USER_AGENT)
    # class="r5a77d"
    # Next in <a>Vermutung</a>
    # spliting data
    information = re.search(r'<a class="fKDtNb" href=(.*?)</a>',
                            response.text).group(1).split('style="font-style:italic">')
    google_search_url = information[0].replace('"', '')
    guess = information[1].title()

    return google_search_url, guess


def reddit_deeplearn_imagetool(ARGS):

    google_search_url, guess = fetch_results("https://i.redd.it/6zgoz90pbpv11.jpg")

    reddit = RedditChecker(
        ARGS.subreddits,
        db_file_path=ARGS.database_path,
        db_type=ARGS.database_type
    )

    reddit_data = generate_reddit_data(reddit, ARGS.reddit_sort, ARGS.reddit_time)

    if ARGS.create_database:
        sql_create_commands = FileReader.read_file(ARGS.database_schema)
        reddit.db_handler.create_db
        reddit.db_handler.init_database(sql_create_commands)

    insert_reddit_data_to_db(reddit.db_handler, reddit_data)

if __name__ == '__main__':
    try:
        reddit_deeplearn_imagetool(arg_parse_info())
    except SystemExit:
        print("Program exit.")
