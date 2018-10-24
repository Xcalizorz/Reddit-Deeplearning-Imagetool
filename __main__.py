from RedditChecker import RedditChecker


def main():
    reddit = RedditChecker('memes')

    reddit_data = reddit.subreddit_data

    print(reddit_data)

if __name__ == '__main__':
    main()
