# -*- coding: utf-8 -*-
from cmd_line_args import arg_parse_info
from core.reddit.api.RedditChecker import RedditChecker
from core.io.FileReader import FileReader
from core.db.reddit import RedditDBHelper


def reddit_deeplearn_imagetool(ARGS):

    reddit = RedditChecker(
        ARGS.subreddits,
        db_file_path=ARGS.database_path,
        db_type=ARGS.database_type
    )

    reddit_data = RedditDBHelper.generate_reddit_data(
        reddit, ARGS.reddit_sort, ARGS.reddit_time
    )

    if ARGS.create_database:
        sql_create_commands = FileReader.read_file(ARGS.database_schema)
        reddit.db_handler.create_db
        reddit.db_handler.init_database(sql_create_commands)

    RedditDBHelper.insert_reddit_data_to_db(reddit.db_handler, reddit_data)

if __name__ == '__main__':
    try:
        reddit_deeplearn_imagetool(arg_parse_info())
    except SystemExit:
        print("Program exit.")
