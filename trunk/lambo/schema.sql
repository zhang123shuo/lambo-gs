-- To create the database:
--   CREATE DATABASE promise;
--   GRANT ALL PRIVILEGES ON promise.* TO 'root'@'localhost' IDENTIFIED BY '123456';
--
-- To reload the tables:
--   mysql --user=root --password=123456 --database=promise --default_character_set=utf8 < schema.sql
SET SESSION storage_engine = "InnoDB";
SET SESSION time_zone = "+0:00";
ALTER DATABASE CHARACTER SET "utf8";

DROP TABLE IF EXISTS entries;
CREATE TABLE entries (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    uid INT NOT NULL REFERENCES users(id), 
    cid INT NOT NULL REFERENCES cats(id), 
    title VARCHAR(512) NOT NULL, 
    content MEDIUMTEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated DATETIME,
    view_count INT NOT NULL DEFAULT 0,
    reply_count INT NOT NULL DEFAULT 0,
    KEY (created)
);



DROP TABLE IF EXISTS tags;
CREATE TABLE tags (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	entry_id INT NOT NULL REFERENCES entries(id), 
	name VARCHAR(100) NOT NULL
);

DROP TABLE IF EXISTS cats;
CREATE TABLE cats (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
	name VARCHAR(100) NOT NULL
);


DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    pwd VARCHAR(100) NOT NULL
);


DROP TABLE IF EXISTS im_msgs;
CREATE TABLE im_msgs (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    uid INT NOT NULL REFERENCES users(id),   
    uname VARCHAR(100) NOT NULL,  
    body MEDIUMTEXT NOT NULL,
    time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    KEY (time)
);

INSERT INTO users(email,name,pwd) VALUES('hongleiming@gmail.com','洪磊明','123456');
INSERT INTO users(email,name,pwd) VALUES('dao@gmail.com','一刀定不了天','123456');
INSERT INTO users(email,name,pwd) VALUES('rushmore@gmail.com','rushmore','123456'); 

INSERT INTO cats(name) VALUES('中证资讯'); 
INSERT INTO cats(name) VALUES('原创交流'); 
INSERT INTO cats(name) VALUES('金融大杂烩'); 
INSERT INTO cats(name) VALUES('站务/建议'); 

