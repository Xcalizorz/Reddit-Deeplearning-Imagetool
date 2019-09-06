CREATE TABLE subreddits (
	id VARCHAR(20) PRIMARY KEY NOT NULL,
	subreddit_name_prefixed VARCHAR(50),
  subreddit_subscribers INT
);

CREATE index subreddit_id on subreddits(id);
CREATE index subreddit_name_prefixed on subreddits(subreddit_name_prefixed);

CREATE TABLE images (
	id VARCHAR(20) PRIMARY KEY NOT NULL,
  subreddit_id INT NOT NULL,
	image_url TEXT,
  permalink TEXT,
  upload_time DATETIME,
  FOREIGN KEY(subreddit_id) REFERENCES subreddits(id)
);

CREATE index image_id on images(id);

CREATE TABLE reddit_sort (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sort varchar(10)
);

CREATE index s_sort on reddit_sort(sort);

CREATE TABLE reddit_time (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sort varchar(10)
);

CREATE index t_sort on reddit_time(sort);

CREATE TABLE image_success (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_id varchar(20) NOT NULL,
    ups INT,
    num_comments INT,
    gid_1 TINYINT,
    gid_2 TINYINT,
    gid_3 TINYINT,
    reddit_sort varchar(10),
    reddit_time varchar(10),
    last_checked DATETIME,
    time_passed TIME,
    FOREIGN KEY(image_id) REFERENCES images(id),
    FOREIGN KEY(reddit_sort) REFERENCES reddit_sort(sort),
    FOREIGN KEY(reddit_time) REFERENCES reddit_time(sort)
);

CREATE index time_passed on image_success(time_passed);

CREATE TABLE image_processing (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_id varchar(20) NOT NULL UNIQUE,
    title varchar(50),
    google_permalink TEXT,
    guess varchar(50),
    first_result TEXT,

    FOREIGN KEY(image_id) REFERENCES images(id)
);

CREATE index guess ON image_processing(guess);

INSERT INTO reddit_sort(sort)
VALUES ('controversial'), ('hot'), ('new'), ('rising'), ('top');

INSERT INTO reddit_time(sort)
VALUES ('hour'), ('day'), ('week'), ('month'), ('year'), ('all');