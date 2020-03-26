create table user(
    QQ INT PRIMARY KEY NOT NULL,
    score int DEFAULT 0,
    diamond int DEFAULT 0,
    ticket int DEFAULT 0,
    sign int DEFAULT 0,
    messageNum int DEFAULT 0
);

create table pokemon(
    QQ INT PRIMARY KEY NOT NULL,
    evelsBall int DEFAULT 0,
    superBall int DEFAULT 0,
    masterBall int DEFAULT 0,
    -- sceneA
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
    menghuan int DEFAULT 0,
    -- sceneB
    lvmaochong int DEFAULT 0,
    dujiaochong int DEFAULT 0,
    lieque int DEFAULT 0,
    chuanshanshu int DEFAULT 0,
    niduolang int DEFAULT 0,
    niduolan int DEFAULT 0,
    maoqiu int DEFAULT 0,
    liuwei int DEFAULT 0,
    kabishou int DEFAULT 0,
    xipanmoou int DEFAULT 0,
    kentailuo int DEFAULT 0,
    feitiantanglang int DEFAULT 0,
    dajia int DEFAULT 0,
    miaowazhongzi int DEFAULT 0,
    xiaohuolong int DEFAULT 0,
    jienigui int DEFAULT 0,
    huoyanniao int DEFAULT 0,
    jidongniao int DEFAULT 0,
    shandianniao int DEFAULT 0,
    chaomeng int DEFAULT 0
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
    (date('now', 'localtime'));


--  alter table user add column messagenum int default 0;
-- alter table pokemon add column lvmaochong int default 0;
-- alter table pokemon add column dujiaochong int default 0;
-- alter table pokemon add column lieque int default 0;
-- alter table pokemon add column chuanshanshu int default 0;
-- alter table pokemon add column niduolang int default 0;
-- alter table pokemon add column niduolan int default 0;
-- alter table pokemon add column maoqiu int default 0;
-- alter table pokemon add column liuwei int default 0;
-- alter table pokemon add column kabishou int default 0;
-- alter table pokemon add column xipanmoou int default 0;
-- alter table pokemon add column kentailuo int default 0;
-- alter table pokemon add column feitiantanglang int default 0;
-- alter table pokemon add column dajia int default 0;
-- alter table pokemon add column miaowazhongzi int default 0;
-- alter table pokemon add column xiaohuolong int default 0;
-- alter table pokemon add column jienigui int default 0;
-- alter table pokemon add column huoyanniao int default 0;
-- alter table pokemon add column jidongniao int default 0;
-- alter table pokemon add column shandianniao int default 0;
-- alter table pokemon add column chaomeng int default 0;
