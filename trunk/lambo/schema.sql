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
    created BIGINT NOT NULL,
	updated BIGINT,
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
    time BIGINT NOT NULL,
    KEY (time)
);

DROP TABLE IF EXISTS hq_quotes;
CREATE TABLE hq_quotes (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,  
    code VARCHAR(10) NOT NULL,  
    name VARCHAR(10) NOT NULL,
    open DECIMAL(4,2),
    closed DECIMAL(4,2),
    price DECIMAL(4,2),
    highest DECIMAL(4,2),
    lowest DECIMAL(4,2),
    ask DECIMAL(4,2),
    bid DECIMAL(4,2),
    volume INT,
    turnover DECIMAL(12,2),
    
    buy1_cnt INT,
    buy1_price DECIMAL(4,2),
    buy2_cnt INT,
    buy2_price DECIMAL(4,2),
    buy3_cnt INT,
    buy3_price DECIMAL(4,2),
    buy4_cnt INT,
    buy4_price DECIMAL(4,2),
    buy5_cnt INT,
    buy5_price DECIMAL(4,2),
    
    sell1_cnt INT,
    sell1_price DECIMAL(4,2),
    sell2_cnt INT,
    sell2_price DECIMAL(4,2),
    sell3_cnt INT,
    sell3_price DECIMAL(4,2),
    sell4_cnt INT,
    sell4_price DECIMAL(4,2),
    sell5_cnt INT,
    sell5_price DECIMAL(4,2),
    
    date DATE,
    time TIME
    
);


INSERT INTO users(email,name,pwd) VALUES('hongleiming@gmail.com','洪磊明','123456');
INSERT INTO users(email,name,pwd) VALUES('dao@gmail.com','一刀定不了天','123456');
INSERT INTO users(email,name,pwd) VALUES('rushmore@gmail.com','rushmore','123456'); 

INSERT INTO cats(name) VALUES('中证资讯'); 
INSERT INTO cats(name) VALUES('原创交流'); 
INSERT INTO cats(name) VALUES('金融大杂烩'); 
INSERT INTO cats(name) VALUES('站务/建议'); 

