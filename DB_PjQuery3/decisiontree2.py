def decisiontree2(host,user,password):
   db = pymysql.connect(host=host, user=user, password=password, db='db2017_6', charset='utf8mb4')
   curs = db.cursor()
   sql1 = '''
            CREATE OR REPLACE VIEW ReputStatMatrix as
                select A.UserId, A.Reputation, A.ActiveDays, B.NumOfPosts, C.NumOfComments, C.CommentScore, D.NumOfBadges
                from (select userinfo.Id as UserId, userinfo.Reputation as Reputation, (userinfo.LastAccessDate - userinfo.CreationDate) as ActiveDays from userinfo) as A,
                (select posts.OwnerUserId, count(posts.Id) as NumOfPosts from posts group by posts.OwnerUserId) as B,
                (select comments.UserInfoId, count(comments.Id) as NumOfComments, sum(comments.score) as CommentScore from comments group by comments.UserInfoId) as C,
                (select badges.UserInfoId, count(badges.Id) as NumOfBadges from badges group by badges.UserInfoId) as D
                where A.UserId=B.OwnerUserId and A.UserId=C.UserInfoId and A.UserId=D.UserInfoId and A.Reputation>110
            '''
            # Add A.ActiveDays, C.CommentScore.
   sql2 = 'select * from ReputStatMatrix'
   curs.execute(sql1)
   df2 = pd.read_sql(sql2, db)
   print(df2)
   db.commit()
   data = np.array(df2)

   # data i/o
   data= pd.DataFrame(df2)
   cols= list(data.columns)
   features= copy.deepcopy(cols)
   features.remove('Reputation')
   # using pandas, mapping y into boolean(true when reputation>180)
   data.insert(len(data.columns), 'HasReputation', (data['Reputation'] > 180))
   data.drop('Reputation', axis=1)
   #Dividing X and y
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
   dt_entropy_graph= tree.export_graphviz(dt_entropy, out_file= None)
   graph_to_render= graphviz.Source(dt_entropy_graph)
