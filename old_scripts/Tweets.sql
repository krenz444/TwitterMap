DROP TABLE IF EXISTS Coordinates;

CREATE TABLE Coordinates(

    id char(36) primary key,
    longitude float,
    latitude float

);

DROP TABLE IF EXISTS Users;

CREATE TABLE Users(

    id bigint primary key,
    created_at nvarchar(255),
    description nvarchar(255),
    favourites_count int,
    followers_count int,
    friends_count int,
    geo_enabled bool,
    lang nvarchar(20),
    listed_count int,
    location nvarchar(255),
    name nvarchar(255),
    protected bool,
    screen_name nvarchar(50),
    statuses_count int,
    time_zone nvarchar(255),
    url nvarchar(255),
    verified bool

);

DROP TABLE IF EXISTS Tweet;

CREATE TABLE Tweet(

    coordinates char(36),
    created_at nvarchar(255),
    filter_level nvarchar(255),
    id bigint,
    in_reply_to_status_id bigint,
    in_reply_to_user_id bigint,
    lang nvarchar(20),
    possibly_sensitive bool,
    retweet_count int,
    retweeted bool,
    retweeted_status int,
    source nvarchar(2184),
    text nvarchar(2184),
    truncated bool,
    user bigint,
    favorite_count int,
    favorited bool,
    
    witheld_copyright bool,
    foreign key(coordinates) references Coordinates(id),    
    foreign key(user) references Users(id)

);
