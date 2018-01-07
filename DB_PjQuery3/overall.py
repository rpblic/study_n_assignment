import csv
import pymysql
import orangecontrib
import pandas as pd
from pandas import DataFrame
from orangecontrib.associate.fpgrowth import *
import numpy as np

def association(host,user,password):
    conn = pymysql.connect(host=host, user=user, password=password)
    try:
        with conn.cursor() as cursor:
            sql = 'CREATE DATABASE IF NOT EXISTS db2017_6'
            cursor.execute(sql)
            conn.commit()
        conn.commit()
    finally:
        conn.close()
    db = pymysql.connect(host=host,user=user,password=password,db='db2017_6',charset='utf8')
    curs = db.cursor()

    # userInfo 테이블 생성
    sql1 = 'CREATE TABLE IF NOT EXISTS userInfo(Id integer NOT NULL,Reputation integer,DisplayName varchar(255),Age integer,CreationDate datetime,LastAccessDate datetime,WebsiteUrl varchar(255), Location varchar(255),AboutMe longtext, PRIMARY KEY(Id))'
    #posts 테이블 생성
    sql2 = 'CREATE TABLE IF NOT EXISTS posts(Id integer NOT NULL,CreationDate datetime,Body longtext,OwnerUserId integer,LasActivityDate datetime,PRIMARY KEY(Id))'
    # badges 테이블 생성
    sql3 = 'CREATE TABLE IF NOT EXISTS badges(Id integer NOT NULL,UserInfoId integer NOT NULL,Name varchar(255),Date datetime,PRIMARY KEY(Id))'
    # comments 테이블 생성
    sql4 = 'CREATE TABLE IF NOT EXISTS comments(Id integer NOT NULL,PostId integer NOT NULL,Score integer,CreationDate datetime,UserInfoId integer NOT NULL,PRIMARY KEY(Id),FOREIGN KEY(UserInfoId) REFERENCES userInfo(Id))'
    # questionPosts_Tags 테이블 생성
    sql5 = 'CREATE TABLE IF NOT EXISTS questionTags(questionPostsId integer NOT NULL,TagName varchar(255) NOT NULL,PRIMARY KEY(questionPostsId,TagName))'
    # 새로운 데이터인 tagname를 저장하기 위해 table tagname을 하고, 데이터를 insert
    sql6 = 'CREATE TABLE IF NOT EXISTS orderedTagName(Id integer NOT NULL,TagName varchar(255) NOT NULL,PRIMARY KEY(Id),UNIQUE(TagName))'

    # curs.execute(sql0)
    curs.execute(sql1)
    curs.execute(sql2)
    curs.execute(sql3)
    curs.execute(sql4)
    curs.execute(sql5)
    curs.execute(sql6)
    db.commit()

    # userinfo 테이블에 데이터 저장을 위한 프레임 생성
    f = open('userInfo.csv', 'r', encoding='utf-8', errors='replace')
    rdr = csv.reader(f)
    next(rdr, None)
    #익명의 사용자가 post를 작성한 경우도 있으므로 foreign key constraint에 어긋나지 않기 위해 userId=0인 경우는 남겨둔다.
    userInfoData = []
    for line in rdr:
        if ((line[3]) == ''):
            line[3] = None
        if ((line[6]) == ''):
            line[6] = None
        if ((line[7]) == ''):
            line[7] = None
        if ((line[8]) == ''):
            line[8] = None
        userInfoData.append(tuple(line))
    userInfoData = tuple(userInfoData)
    f.close()

    # posts 테이블에 데이터 저장을 위한 프레임 생성
    f = open('posts.csv', 'r', encoding='utf-8', errors='replace')
    rdr = csv.reader(f)
    next(rdr, None)
    postsData = []
    for line in rdr:
        if ((line[2]) == ''):
            line[2] = None
        postsData.append(tuple(line))
    postsData = tuple(postsData)
    f.close()

    # badges 테이블에 데이터 저장을 위한 프레임 생성
    f = open('badges.csv', 'r', encoding='utf-8', errors='replace')
    rdr = csv.reader(f)
    next(rdr, None)
    badgesData = []
    for line in rdr:
        badgesData.append(tuple(line))
    badgesData = tuple(badgesData)
    # comments 테이블에 데이터 저장을 위한 프레임 생성
    f = open('comments.csv', 'r', encoding='utf-8', errors='replace')
    f1 = csv.reader(f)
    next(f1, None)
    comments = []

    for line in f1:
        for i in (0, 1, 2, 4):
            if line[i] != "":
                line[i] = int(line[i])
            else:
                line[i] = None
        if line[3] == "":
            line[3] = None
        comments.append(line)

    f.close()


    # questionTags 테이블에 데이터 저장을 위한 프레임 생성
    f=open('questionPosts.csv','r', encoding='utf-8', errors='replace')
    rdr=csv.reader(f)
    next(rdr, None)
    questionTagsData=[]
    tagName = ''
    for line in rdr:
        #question에 해당하는 tag가 없는 경우 넘어간다.(tag는 null이 가능하다고 가정)
        if ((line[5]) == ''):
            continue
        for c in line[5]:
            if(c=='<'):
                continue
            if (c == '>'):
                qId_tagName = (line[0], tagName)
                questionTagsData.append(qId_tagName)
                tagName = ''
                continue
            tagName=tagName+c
    f.close()


    # orderedTagName 테이블에 데이터 저장을 위한 프레임 생성
    f = open('tagname.csv', 'r', encoding='utf-8', errors='replace')
    rdr = csv.reader(f)
    next(rdr, None)
    tagname = []

    for line in rdr:
        if line[0] != "":
            line[0] = int(line[0])
        else:
            line[0] = None
        if line[1] == "":
            line[1] = None
        tagname.append(line)

    f.close()

    conn = pymysql.connect(host=host, user=user, password=password, db='db2017_6', charset='utf8')
    curs = conn.cursor()

    # userInfo 테이블에 데이터 입력
    sql = '''insert ignore into userInfo
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
    curs.executemany(sql, userInfoData)
    conn.commit()

    # posts 테이블에 데이터 입력
    sql = '''insert ignore into posts VALUES(%s,%s,%s,%s,%s); '''
    curs.executemany(sql, postsData)
    conn.commit()

    # badges 테이블에 데이터 입력
    sql = '''insert ignore into badges VALUES(%s,%s,%s,%s); '''
    curs.executemany(sql, badgesData)
    conn.commit()

    # questionTags 테이블에 데이터 입력
    sql = '''insert ignore into questionTags VALUES(%s,%s); '''
    curs.executemany(sql, questionTagsData)
    conn.commit()

    # comments 테이블에 데이터 입력
    sql='''insert ignore into comments VALUES(%s,%s,%s,%s,%s); '''
    curs.executemany(sql, comments)
    conn.commit()

    # orderedTagName 테이블에 데이터 입력
    sql = '''insert ignore into orderedTagName(Id,TagName) values (%s,%s); '''
    curs.executemany(sql, tagname)
    conn.commit()
    conn.close()


    db = pymysql.connect(host=host, user=user, password=password, db='db2017_6', charset='utf8mb4')
    curs = db.cursor()
    sql7 = 'CREATE OR REPLACE VIEW TagMatrix as SELECT questionPostsId,SUM(IF(id=1,1,0)),SUM(IF(id=2,1,0)),SUM(IF(id=3,1,0)),SUM(IF(id=4,1,0)),SUM(IF(id=5,1,0)),SUM(IF(id=6,1,0)),SUM(IF(id=7,1,0)),SUM(IF(id=8,1,0)),SUM(IF(id=9,1,0)),SUM(IF(id=10,1,0)),SUM(IF(id=11,1,0)),SUM(IF(id=12,1,0)),SUM(IF(id=13,1,0)),SUM(IF(id=14,1,0)),SUM(IF(id=15,1,0)),SUM(IF(id=16,1,0)),SUM(IF(id=17,1,0)),SUM(IF(id=18,1,0)),SUM(IF(id=19,1,0)),SUM(IF(id=20,1,0)),SUM(IF(id=21,1,0)),SUM(IF(id=22,1,0)),SUM(IF(id=23,1,0)),SUM(IF(id=24,1,0)),SUM(IF(id=25,1,0)),SUM(IF(id=26,1,0)),SUM(IF(id=27,1,0)),SUM(IF(id=28,1,0)),SUM(IF(id=29,1,0)),SUM(IF(id=30,1,0)),SUM(IF(id=31,1,0)),SUM(IF(id=32,1,0)),SUM(IF(id=33,1,0)),SUM(IF(id=34,1,0)),SUM(IF(id=35,1,0)),SUM(IF(id=36,1,0)),SUM(IF(id=37,1,0)),SUM(IF(id=38,1,0)),SUM(IF(id=39,1,0)),SUM(IF(id=40,1,0)),SUM(IF(id=41,1,0)),SUM(IF(id=42,1,0)),SUM(IF(id=43,1,0)),SUM(IF(id=44,1,0)),SUM(IF(id=45,1,0)),SUM(IF(id=46,1,0)),SUM(IF(id=47,1,0)),SUM(IF(id=48,1,0)),SUM(IF(id=49,1,0)),SUM(IF(id=50,1,0)),SUM(IF(id=51,1,0)),SUM(IF(id=52,1,0)),SUM(IF(id=53,1,0)),SUM(IF(id=54,1,0)),SUM(IF(id=55,1,0)),SUM(IF(id=56,1,0)),SUM(IF(id=57,1,0)),SUM(IF(id=58,1,0)),SUM(IF(id=59,1,0)),SUM(IF(id=60,1,0)),SUM(IF(id=61,1,0)),SUM(IF(id=62,1,0)),SUM(IF(id=63,1,0)),SUM(IF(id=64,1,0)),SUM(IF(id=65,1,0)),SUM(IF(id=66,1,0)),SUM(IF(id=67,1,0)),SUM(IF(id=68,1,0)),SUM(IF(id=69,1,0)),SUM(IF(id=70,1,0)),SUM(IF(id=71,1,0)),SUM(IF(id=72,1,0)),SUM(IF(id=73,1,0)),SUM(IF(id=74,1,0)),SUM(IF(id=75,1,0)),SUM(IF(id=76,1,0)),SUM(IF(id=77,1,0)),SUM(IF(id=78,1,0)),SUM(IF(id=79,1,0)),SUM(IF(id=80,1,0)),SUM(IF(id=81,1,0)),SUM(IF(id=82,1,0)),SUM(IF(id=83,1,0)),SUM(IF(id=84,1,0)),SUM(IF(id=85,1,0)),SUM(IF(id=86,1,0)),SUM(IF(id=87,1,0)),SUM(IF(id=88,1,0)),SUM(IF(id=89,1,0)),SUM(IF(id=90,1,0)),SUM(IF(id=91,1,0)),SUM(IF(id=92,1,0)),SUM(IF(id=93,1,0)),SUM(IF(id=94,1,0)),SUM(IF(id=95,1,0)),SUM(IF(id=96,1,0)),SUM(IF(id=97,1,0)),SUM(IF(id=98,1,0)),SUM(IF(id=99,1,0)),SUM(IF(id=100,1,0)) FROM questionTags, orderedTagName WHERE questionTags.TagName=orderedTagName.TagName GROUP BY questionPostsId'
    sql8 = 'SELECT * FROM TagMatrix'
    curs.execute(sql7)
    df = pd.read_sql(sql8, db)
    # print(df)
    db.commit()

# df를 numpy의 array로 바꾼 후 첫번째 column인 questionId를 제거
data = np.array(df)[:, 1:]
X = data.astype(int)
print(frequent_itemsets(X, 0.01))
itemsets = dict(frequent_itemsets(X, 0.01))
print(itemsets)
rules = association_rules(itemsets, 0.05)
rules = list(rules)
print(rules)

#R1
def requirement6(host,user,password):

    db = pymysql.connect(host=host, user=user, password=password, db='db2017_6', charset='utf8mb4')
    curs = db.cursor()
    sql7='CREATE OR REPLACE VIEW TagMatrix as SELECT questionPostsId,SUM(IF(id=1,1,0)),SUM(IF(id=2,1,0)),SUM(IF(id=3,1,0)),SUM(IF(id=4,1,0)),SUM(IF(id=5,1,0)),SUM(IF(id=6,1,0)),SUM(IF(id=7,1,0)),SUM(IF(id=8,1,0)),SUM(IF(id=9,1,0)),SUM(IF(id=10,1,0)),SUM(IF(id=11,1,0)),SUM(IF(id=12,1,0)),SUM(IF(id=13,1,0)),SUM(IF(id=14,1,0)),SUM(IF(id=15,1,0)),SUM(IF(id=16,1,0)),SUM(IF(id=17,1,0)),SUM(IF(id=18,1,0)),SUM(IF(id=19,1,0)),SUM(IF(id=20,1,0)),SUM(IF(id=21,1,0)),SUM(IF(id=22,1,0)),SUM(IF(id=23,1,0)),SUM(IF(id=24,1,0)),SUM(IF(id=25,1,0)),SUM(IF(id=26,1,0)),SUM(IF(id=27,1,0)),SUM(IF(id=28,1,0)),SUM(IF(id=29,1,0)),SUM(IF(id=30,1,0)),SUM(IF(id=31,1,0)),SUM(IF(id=32,1,0)),SUM(IF(id=33,1,0)),SUM(IF(id=34,1,0)),SUM(IF(id=35,1,0)),SUM(IF(id=36,1,0)),SUM(IF(id=37,1,0)),SUM(IF(id=38,1,0)),SUM(IF(id=39,1,0)),SUM(IF(id=40,1,0)),SUM(IF(id=41,1,0)),SUM(IF(id=42,1,0)),SUM(IF(id=43,1,0)),SUM(IF(id=44,1,0)),SUM(IF(id=45,1,0)),SUM(IF(id=46,1,0)),SUM(IF(id=47,1,0)),SUM(IF(id=48,1,0)),SUM(IF(id=49,1,0)),SUM(IF(id=50,1,0)),SUM(IF(id=51,1,0)),SUM(IF(id=52,1,0)),SUM(IF(id=53,1,0)),SUM(IF(id=54,1,0)),SUM(IF(id=55,1,0)),SUM(IF(id=56,1,0)),SUM(IF(id=57,1,0)),SUM(IF(id=58,1,0)),SUM(IF(id=59,1,0)),SUM(IF(id=60,1,0)),SUM(IF(id=61,1,0)),SUM(IF(id=62,1,0)),SUM(IF(id=63,1,0)),SUM(IF(id=64,1,0)),SUM(IF(id=65,1,0)),SUM(IF(id=66,1,0)),SUM(IF(id=67,1,0)),SUM(IF(id=68,1,0)),SUM(IF(id=69,1,0)),SUM(IF(id=70,1,0)),SUM(IF(id=71,1,0)),SUM(IF(id=72,1,0)),SUM(IF(id=73,1,0)),SUM(IF(id=74,1,0)),SUM(IF(id=75,1,0)),SUM(IF(id=76,1,0)),SUM(IF(id=77,1,0)),SUM(IF(id=78,1,0)),SUM(IF(id=79,1,0)),SUM(IF(id=80,1,0)),SUM(IF(id=81,1,0)),SUM(IF(id=82,1,0)),SUM(IF(id=83,1,0)),SUM(IF(id=84,1,0)),SUM(IF(id=85,1,0)),SUM(IF(id=86,1,0)),SUM(IF(id=87,1,0)),SUM(IF(id=88,1,0)),SUM(IF(id=89,1,0)),SUM(IF(id=90,1,0)),SUM(IF(id=91,1,0)),SUM(IF(id=92,1,0)),SUM(IF(id=93,1,0)),SUM(IF(id=94,1,0)),SUM(IF(id=95,1,0)),SUM(IF(id=96,1,0)),SUM(IF(id=97,1,0)),SUM(IF(id=98,1,0)),SUM(IF(id=99,1,0)),SUM(IF(id=100,1,0)) FROM questionTags, orderedTagName WHERE questionTags.TagName=orderedTagName.TagName GROUP BY questionPostsId'
    sql8='SELECT * FROM TagMatrix'
    curs.execute(sql7)
    df=pd.read_sql(sql8,db)
    # print(df)
    db.commit()

    #df를 numpy의 array로 바꾼 후 첫번째 column인 questionId를 제거
    data = np.array(df)[:, 1:]
    X = data.astype(int)
    print(frequent_itemsets(X, 0.01))
    itemsets = dict(frequent_itemsets(X, 0.01))
    print(itemsets)
    rules = association_rules(itemsets, 0.05)
    rules = list(rules)
    print(rules)

#R2
def requirement7(host,user,password):
    import pymysql
    import csv
    import pandas as pd
    from pandas import DataFrame

    db = pymysql.connect(host=host, user=user, password=password, db='db2017_6', charset='utf8mb4')
    curs = db.cursor()
    sql1 = 'CREATE OR REPLACE VIEW ReputStatMatrix as select A.UserId, A.Reputation, B.NumOfPosts, C.NumOfComments, D.NumOfBadges from (select userinfo.Id as UserId, userinfo.Reputation as Reputation from userinfo) as A,(select posts.OwnerUserId, count(posts.Id) as NumOfPosts from posts group by posts.OwnerUserId) as B, (select comments.UserInfoId, count(comments.Id) as NumOfComments from comments group by comments.UserInfoId) as C, (select badges.UserInfoId, count(badges.Id) as NumOfBadges from badges group by badges.UserInfoId) as D where A.UserId=B.OwnerUserId and A.UserId=C.UserInfoId and A.UserId=D.UserInfoId and A.Reputation>110'
    sql2 = 'select * from ReputStatMatrix'
    curs.execute(sql1)
    df2 = pd.read_sql(sql2, db)
    print(df2)
    db.commit()

# association('localhost', 'root', '1234')
# requirement6('localhost', 'root', '1234')
# requirement7('localhost', 'root', '1234')
from sklearn.tree import DecisionTreeClassifier
import numpy as np
import pandas as pd
# import graphviz
# import pymysql

# get a file in DB
#define data_raw

# using pandas, mapping y into 0, 1 when reputation>180
features= ['NumOfPosts', 'NumOfComments', 'NumOfBadges']
cols= ['Reputation']
cols.extend(features)

data= pd.DataFrame(data_raw, columns= cols)
data.insert(len(data.columns), 'HasReputation', (data['Reputation'] > 180))
print(data)

#defining data_to_predict
data_to_predict_dict= {
                        'NumOfPosts': [5, 2, 6],
                        'NumOfComments': [5, 6, 3],
                        'NumOfBadges': [5, 18, 10],
                        }
data_to_predict= pd.DataFrame(data_to_predict_dict, columns= features)
print(data_to_predict)

y= pd.DataFrame(data["HasReputation"], columns= ['HasReputation'])
X= data[features]
print(X)
print(y)

# DO DTClassifier
dt_gini= DecisionTreeClassifier(criterion="gini", min_samples_split=10)
dt_gini.fit(X, y)
dt_entropy= DecisionTreeClassifier(criterion="entropy", min_samples_split=10)
dt_entropy.fit(X, y)
print("for the case gini: ", dt_gini.predict(data_to_predict), '\t',\
                                dt_gini.predict_proba(data_to_predict))
print("for the case entropy: ", dt_entropy.predict(data_to_predict), '\t',\
                                dt_entropy.predict_proba(data_to_predict))

# DO graphviz
dt_gini_graph= tree.export_graphviz(dt_gini, out_file= None)
graph_to_render= graphviz.Source(dt_gini_graph)
graph_to_render.render("result_decision_tree_gini")
dt_gini_graph= tree.export_graphviz(dt_entropy, out_file= None)
graph_to_render= graphviz.Source(dt_entropy_graph)
graph_to_render.render("result_decision_tree_entropy")
