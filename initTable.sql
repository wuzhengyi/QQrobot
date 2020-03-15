create table user(
    QQ INT PRIMARY KEY NOT NULL,
    score int DEFAULT 0,
    diamond int DEFAULT 0,
    ticket int DEFAULT 0,
    sign int DEFAULT 0
);

create table pokemon(
    QQ INT PRIMARY KEY NOT NULL,
    evelsBall int DEFAULT 0,
    superBall int DEFAULT 0,
    masterBall int DEFAULT 0,
    xiaolada int DEFAULT 0,
    bobo int DEFAULT 0,
    miaomiao int DEFAULT 0,
    wasidan int DEFAULT 0,
    apashe int DEFAULT 0,
    dashetou int DEFAULT 0,
    pikaqiu int DEFAULT 0,
    pipi int DEFAULT 0,
    pangding int DEFAULT 0,
    yibu int DEFAULT 0,
    jilidan int DEFAULT 0,
    dailong int DEFAULT 0,
    menghuan int DEFAULT 0
);

create table constellation(
    QQ INT PRIMARY KEY NOT NULL,
    Aries int DEFAULT 0,
    Taurus int DEFAULT 0,
    Gemini int DEFAULT 0,
    Cancer int DEFAULT 0,
    Leo int DEFAULT 0,
    Virgo int DEFAULT 0,
    Libra int DEFAULT 0,
    Scorpio int DEFAULT 0,
    Sagittarius int DEFAULT 0,
    Capricorn int DEFAULT 0,
    Aquarius int DEFAULT 0,
    Pisces int DEFAULT 0
);

create table common(
    signDate INT PRIMARY KEY NOT NULL,
    signNum INT DEFAULT 0
);

INSERT INTO
    common (signDate)
VALUES
    (date('now'));