import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
path_name= os.path.dirname(__file__)
os.chdir(path_name)

def get_XY(file_name):
    rawData= pd.read_csv(file_name)
    # rawData.info()
    # RangeIndex: 891 entries, 0 to 890
    # Data columns (total 12 columns):
    # PassengerId    891 non-null int64
    # Survived       891 non-null int64
    # Pclass         891 non-null int64
    # Name           891 non-null object
    # Sex            891 non-null object
    # Age            714 non-null float64
    # SibSp          891 non-null int64
    # Parch          891 non-null int64
    # Ticket         891 non-null object
    # Fare           891 non-null float64
    # Cabin          204 non-null object
    # Embarked       889 non-null object
    # dtypes: float64(2), int64(5), object(5)


    print(rawData.isnull().sum())       # How to consider NaN data?
    # PassengerId      0
    # Survived         0
    # Pclass           0
    # Name             0
    # Sex              0
    # Age            177
    # SibSp            0
    # Parch            0
    # Ticket           0
    # Fare             0
    # Cabin          687
    # Embarked         2
    rawData['Cabin'].fillna('No_Cabin', inplace= True)
    rawData['Null_inAge']= rawData['Age'].isnull()
    rawData['Age'].fillna(0, inplace= True)
    rawData= rawData[rawData['Embarked'].isnull() == False]
    print(rawData['Cabin'].unique())
    # ['No_Cabin' 'C85' 'C123' 'E46' 'G6' 'C103' 'D56' 'A6' 'C23 C25 C27' 'B78'
    #  'D33' 'B30' 'C52' 'C83' 'F33' 'F G73' 'E31' 'A5' 'D10 D12' 'D26' 'C110'
    #  'B58 B60' 'E101' 'F E69' 'D47' 'B86' 'F2' 'C2' 'E33' 'B19' 'A7' 'C49' 'F4'
    #  'A32' 'B4' 'B80' 'A31' 'D36' 'D15' 'C93' 'C78' 'D35' 'C87' 'B77' 'E67'
    #  'B94' 'C125' 'C99' 'C118' 'D7' 'A19' 'B49' 'D' 'C22 C26' 'C106' 'C65'
    #  'E36' 'C54' 'B57 B59 B63 B66' 'C7' 'E34' 'C32' 'B18' 'C124' 'C91' 'E40'
    #  'T' 'C128' 'D37' 'B35' 'E50' 'C82' 'B96 B98' 'E10' 'E44' 'A34' 'C104'
    #  'C111' 'C92' 'E38' 'D21' 'E12' 'E63' 'A14' 'B37' 'C30' 'D20' 'B79' 'E25'
    #  'D46' 'B73' 'C95' 'B38' 'B39' 'B22' 'C86' 'C70' 'A16' 'C101' 'C68' 'A10'
    #  'E68' 'B41' 'A20' 'D19' 'D50' 'D9' 'A23' 'B50' 'A26' 'D48' 'E58' 'C126'
    #  'B71' 'B51 B53 B55' 'D49' 'B5' 'B20' 'F G63' 'C62 C64' 'E24' 'C90' 'C45'
    #  'E8' 'B101' 'D45' 'C46' 'D30' 'E121' 'D11' 'E77' 'F38' 'B3' 'D6' 'B82 B84'
    #  'D17' 'A36' 'B102' 'B69' 'E49' 'C47' 'D28' 'E17' 'A24' 'C50' 'B42' 'C148']
    Cabin_char= lambda x: x[0]+str(len(x.split()))
    rawData['Cabin']= rawData['Cabin'].map(Cabin_char)
    # ['N1' 'C1' 'E1' 'G1' 'D1' 'A1' 'C3' 'B1' 'F1' 'F2' 'D2' 'B2' 'C2' 'B4' 'T1'
    #  'B3']
    # print(rawData.head(10))
    #    PassengerId  Survived  Pclass  \
    # 0            1         0       3
    # 1            2         1       1
    # 2            3         1       3
    # 3            4         1       1
    # 4            5         0       3
    # 5            6         0       3
    # 6            7         0       1
    # 7            8         0       3
    # 8            9         1       3
    # 9           10         1       2
    #
    #                                                 Name     Sex   Age  SibSp  \
    # 0                            Braund, Mr. Owen Harris    male  22.0      1
    # 1  Cumings, Mrs. John Bradley (Florence Briggs Th...  female  38.0      1
    # 2                             Heikkinen, Miss. Laina  female  26.0      0
    # 3       Futrelle, Mrs. Jacques Heath (Lily May Peel)  female  35.0      1
    # 4                           Allen, Mr. William Henry    male  35.0      0
    # 5                                   Moran, Mr. James    male   NaN      0
    # 6                            McCarthy, Mr. Timothy J    male  54.0      0
    # 7                     Palsson, Master. Gosta Leonard    male   2.0      3
    # 8  Johnson, Mrs. Oscar W (Elisabeth Vilhelmina Berg)  female  27.0      0
    # 9                Nasser, Mrs. Nicholas (Adele Achem)  female  14.0      1
    #
    #    Parch            Ticket     Fare     Cabin Embarked
    # 0      0         A/5 21171   7.2500  No_Cabin        S
    # 1      0          PC 17599  71.2833       C85        C
    # 2      0  STON/O2. 3101282   7.9250  No_Cabin        S
    # 3      0            113803  53.1000      C123        S
    # 4      0            373450   8.0500  No_Cabin        S
    # 5      0            330877   8.4583  No_Cabin        Q
    # 6      0             17463  51.8625       E46        S
    # 7      1            349909  21.0750  No_Cabin        S
    # 8      2            347742  11.1333  No_Cabin        S
    # 9      0            237736  30.0708  No_Cabin        C
    if 'Survived' in rawData.columns:
        y= rawData['Survived']
        X= rawData.drop(['PassengerId', 'Survived', 'Name', 'Ticket'], axis= 1)
    else:
        y= rawData['PassengerId']
        X= rawData.drop(['PassengerId', 'Name', 'Ticket'], axis= 1)
    X= pd.get_dummies(X)
    # X.info()
    print(X.isnull().sum())     # NaN check
    return(X, y)

# Main ########################################################################

X, y= get_XY('train.csv')
X_test, PassengerId_test= get_XY('test.csv')
print(X.columns)
print(X_test.columns)
# Index(['Pclass', 'Age', 'SibSp', 'Parch', 'Fare', 'Sex_female', 'Sex_male',
#        'Cabin_A1', 'Cabin_B1', 'Cabin_B2', 'Cabin_B3', 'Cabin_B4', 'Cabin_C1',
#        'Cabin_C2', 'Cabin_C3', 'Cabin_D1', 'Cabin_D2', 'Cabin_E1', 'Cabin_F1',
#        'Cabin_F2', 'Cabin_G1', 'Cabin_N1', 'Cabin_T1', 'Embarked_C',
#        'Embarked_Q', 'Embarked_S'],
#       dtype='object')
# Index(['Pclass', 'Age', 'SibSp', 'Parch', 'Fare', 'Sex_female', 'Sex_male',
#        'Cabin_A1', 'Cabin_B1', 'Cabin_B2', 'Cabin_B3', 'Cabin_B4', 'Cabin_C1',
#        'Cabin_C2', 'Cabin_C3', 'Cabin_D1', 'Cabin_D2', 'Cabin_E1', 'Cabin_E2',
#        'Cabin_F1', 'Cabin_F2', 'Cabin_G1', 'Cabin_N1', 'Embarked_C',
#        'Embarked_Q', 'Embarked_S'],
#       dtype='object')
X_test['Cabin_E1']= X_test['Cabin_E1']+ X_test['Cabin_E2']
X_test= X_test.drop('Cabin_E2', axis= 1)
X_test['Cabin_T1']= 0
X_test['Fare'].fillna(0, inplace= True)
print(X_test.head(10))

clf5= RandomForestClassifier(criterion= "entropy", max_depth= 5, random_state= 50)
clf5.fit(X, y)
clf5_result= pd.Series(clf5.predict(X_test), name= 'Survived')

clf20= RandomForestClassifier(criterion= "entropy", max_depth= 20, random_state= 50)
clf20.fit(X, y)
clf20_result= pd.Series(clf20.predict(X_test), name= 'Survived')

clf_dt5= DecisionTreeClassifier(criterion= "entropy", max_depth= 5, random_state= 50)
clf_dt5.fit(X, y)
clf_dt5_result= pd.Series(clf_dt5.predict(X_test), name= 'Survived')

clf_dt20= DecisionTreeClassifier(criterion= "entropy", max_depth= 20, random_state= 50)
clf_dt20.fit(X, y)
clf_dt20_result= pd.Series(clf_dt20.predict(X_test), name= 'Survived')

result_of_test= pd.concat([PassengerId_test, clf5_result], axis=1)
print(result_of_test.head(30))
result_of_test.to_csv('result_rf5.csv', index= False)
# Score: 0.78468

result_of_test= pd.concat([PassengerId_test, clf20_result], axis=1)
result_of_test.to_csv('result_rf20.csv', index= False)
# Score: 0.73684

result_of_test= pd.concat([PassengerId_test, clf_dt5_result], axis=1)
result_of_test.to_csv('result_dt5.csv', index= False)
# Score: 0.73205

result_of_test= pd.concat([PassengerId_test, clf_dt20_result], axis=1)
result_of_test.to_csv('result_dt20.csv', index= False)
# Score: 0.64593
