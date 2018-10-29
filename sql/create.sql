CREATE TABLE subreddits (
	id VARCHAR(20) PRIMARY KEY NOT NULL,
	subreddit VARCHAR(50),
    subscriber_number BIGINT,
    images_tested INT
);

CREATE index subreddit_id on subreddits(id);
CREATE index subreddit on subreddits(subreddit);

CREATE TABLE images (
	id VARCHAR(20) PRIMARY KEY NOT NULL,
    subreddit_id INT NOT NULL,
	image_url TEXT,
    permalink TEXT,
    upload_time DATETIME,
    FOREIGN KEY(subreddit_id) REFERENCES subreddits(id)
);

CREATE index image_id on images(id);

CREATE TABLE image_success (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_id INT NOT NULL,
    upvotes INT,
    downvotes INT,
    comments INT,
    reddit_gold INT,
    last_checked DATETIME,
    time_passed TIME,
    FOREIGN KEY(image_id) REFERENCES images(id)
);

CREATE index time_passed on image_success(time_passed);

CREATE TABLE image_processing (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    process_result TEXT,
    image_id INT NOT NULL,

    FOREIGN KEY(image_id) REFERENCES images(id)
);

CREATE index process_result on image_processing(process_result);