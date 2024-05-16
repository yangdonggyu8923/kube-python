from dataclasses import dataclass
# from icecream import ic
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold, cross_val_score
from app.api.context.data_sets import DataSets
from app.api.context.models import Models


@dataclass
class TitanicModel(object):

    model = Models()
    dataset = DataSets()

    def preprocess(self, train_fname, test_fname) -> DataSets: # 머신러닝 전처리
        this = self.dataset
        that = self.model
        path = 'C:\\Users\\bitcamp\\python-kube\\chat-server\\backend\\app\\api\\context\\data\\'
        feature = ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked']
        # 데이터셋은 train과 test, validation 3종류로 나뉘어져 있다.
        
        this.train = that.new_dataframe_no_index(train_fname)
        this.test = that.new_dataframe_no_index(test_fname)
        this.id = this.test['PassengerId']
        this.label = this.train['Survived']
        
        # this.train = self.drop_feature_in_train(this, 'Survived')
        # this = self.drop_feature(this, 'Ticket', 'SibSp', 'Parch', 'Cabin' )
        self.drop_feature(this, 'SibSp', 'Parch', 'Ticket', 'Cabin')
        
        
        
        this = self.extract_title_from_name(this)
        
        title_mapping = self.remove_duplicate_title(this)

        
        this = self.title_nominal(this, title_mapping)
        self.drop_feature(this, 'Name')
        self.df_info(this)
        if 'Unnamed: 12' in this.train.columns:
            this.train = this.train.drop(columns=['Unnamed: 12'])
    
        this = self.age_ratio(this)
        this = self.drop_feature(this, 'Age')
    
        this = self.sex_nominal(this)
        this = self.drop_feature(this, 'Sex')

        this = self.embarked_nominal(this)
       
        # this = self.pclass_ordinal(this)
       
        this = self.fare_ratio(this)
        this = self.drop_feature(this, 'Fare')
        this.train = this.train.drop(['Survived'], axis=1)
        
        
        k_fold = self.create_k_fold()
        accuracy = self.get_accuracy(this,k_fold)
        print(accuracy)
        


        return this
    

    def df_info(self, this):
        print('='*50)
        print(f'1. Train 의 type 은 {type(this.train)} 이다.')
        print(f'2. Train 의 column 은 {this.train.columns} 이다.')
        print(f'3. Train 의 상위 1개의 데이터는 {this.train.head()} 이다.')
        print(f'4. Train 의 null 의 갯수는 {this.train.isnull().sum()} 이다.')
        print(f'5. Test 의 type 은 {type(this.test)} 이다.')
        print(f'6. Test 의 column 은 {this.test.columns} 이다.')
        print(f'7. Test 의 상위 1개의 데이터는 {this.test.head()} 이다.')
        print(f'8. Test 의 null 의 갯수는 {this.test.isnull().sum()} 이다.')
        print('='*50)


    @staticmethod
    def drop_feature_in_train(this, *feature) -> object:
        [i.drop(j, axis=1, inplace=True) for j in feature for i in [this.train]]
        return this

    @staticmethod
    def drop_feature_in_test(this, *feature) -> object:
        [i.drop(j, axis=1, inplace=True) for j in feature for i in [this.test]]
        return this


        
    # for i in feature:
    #     this.train = this.train.drop([i], axis=1)
    #     this.test = this.test.drop([i], axis=1)
    
    # for i in [this.train, this.test]:
    #     for j in feature:
    #         i.drop(j, axis=1, inplace=True)
    
    # [i.drop(j, axis=1, inplace=True) for j in feature for i in [this.train, this.test]]
    
    @staticmethod
    def drop_feature(this, *feature) -> object:
        [i.drop([*feature], axis=1, inplace=True) for i in [this.train, this.test]]
        return this
    
    @staticmethod
    def extract_title_from_name(this) -> pd.DataFrame:
        for these in [this.train, this.test]:
            these['Title'] = these['Name'].str.extract('([A-Za-z]+)\.', expand=False)
        return this
    
    @staticmethod
    def remove_duplicate_title(this) -> pd.DataFrame:
        a =[]
        for these in [this.train, this.test]:
            a += list(set(these['Title']))
        a = list(set(a))
        print(a)
        '''
        a = ['Mr', 'Sir', 'Major', 'Don', 'Rev', 'Countess', 'Lady', 'Jonkheer', 'Dr',
        'Miss', 'Col', 'Ms', 'Dona', 'Mlle', 'Mme', 'Mrs', 'Master', 'Capt']
        Royal : ['Countess', 'Lady', 'Sir']
        Rare : ['Capt','Col','Don','Dr','Major','Rev','Jonkheer','Dona','Mme' ]
        Mr : ['Mlle']
        Ms : ['Miss']
        Master
        Mrs
        '''
        title_mapping = {'Mr':1, 'Ms':2, 'Mrs':3, 'Master':4, 'Royal':5, 'Rare':6 }
        return title_mapping

    @staticmethod
    def title_nominal(this, title_mapping) -> pd.DataFrame:
        for these in [this.train, this.test]:
            these['Title'] = these['Title'].replace(['Countess', 'Lady', 'Sir'], 'Royal')
            these['Title'] = these['Title'].replace(['Capt','Col','Don','Dr','Major','Rev','Jonkheer','Dona','Mme'], 'Rare')
            these['Title'] = these['Title'].replace(['Mlle'], 'Mr')
            these['Title'] = these['Title'].replace(['Miss'], 'Ms')
            # Master 는 변화없음
            # Mrs 는 변화없음
            these['Title'] = these['Title'].fillna(0)
            these['Title'] = these['Title'].map(title_mapping)
        return this

    @staticmethod
    def pclass_ordinal(this) -> pd.DataFrame:
        return this
    
    @staticmethod
    def name_nominal(this) -> pd.DataFrame:
        return this
    
    @staticmethod
    def sex_nominal(this) -> pd.DataFrame:
        sex_mapping = {'male':0, 'female':1}
        for these in [this.train, this.test]:
            these['SexNum'] = these['Sex'].map(sex_mapping)

        return this
    
    @staticmethod
    def age_ratio(this) -> pd.DataFrame:
        train = this.train
        test = this.test
        age_mapping = {'Unknown':0 , 'Baby': 1, 'Child': 2, 'Teenager' : 3, 'Student': 4,
                       'Young Adult': 5, 'Adult':6,  'Senior': 7}
        train['Age'] = train['Age'].fillna(-0.5)
        test['Age'] = test['Age'].fillna(-0.5) # 왜 NaN 값에 -0.5 를 할당할까요 ?
        bins = [-1, 0, 5, 12, 18, 24, 35, 60, np.inf] # 이것을 이해해보세요
        labels = ['Unknown', 'Baby', 'Child', 'Teenager', 'Student', 'Young Adult', 'Adult', 'Senior']

        for these in [this.train, this.test]:
            # pd.cut()을 사용하시오. 다른 곳은 고치지 말고 다음 두 줄만 완성하시오
            these['Age'] = pd.cut(these['Age'], bins, labels=labels) # 숫자 -> 문자
            these['AgeGroup'] = these['Age'].map(age_mapping) # map() 사용해서 문자 -> 숫자
        return this
    
    @staticmethod
    def fare_ratio(this) -> pd.DataFrame:
        fare_mapping = {'Unknown':0 , 'Low': 1, 'Middle': 2, 'High' : 3}
        label = {'Unknown', 'Low', 'Middle', 'High'}
        this.train['Fare'] = this.train['Fare'].fillna(-0.5)
        this.test['Fare'] = this.test['Fare'].fillna(-0.5)
        bins = [-1, 8, 15, 31, np.inf]
        for these in [this.train, this.test]:
            these['FareBand'] = pd.cut(these['Fare'], bins, labels=label)
            these['FareBand'] = these['FareBand'].map(fare_mapping)            
        return this
    
    @staticmethod
    def embarked_nominal(this) -> pd.DataFrame:
        train = this.train
        test = this.test
        embarked_mapping = {'-':0, 'S':1, 'Q':2, 'C':3}
        train['Embarked'] = train['Embarked'].fillna('-')
        test['Embarked'] = test['Embarked'].fillna('-')
        for these in train, test:
            these['Embarked'] = these['Embarked'].map(embarked_mapping)
        return this

    @staticmethod
    def create_k_fold() -> object:
        return KFold(n_splits=10, shuffle=True, random_state=0)
    
    @staticmethod
    def learning(self, train_fname, test_fname) -> object:
        this = self.preprocess(train_fname, test_fname)
        print(f'학습 시작')
        k_fold = self.create_k_fold()
        # ic(f'사이킷런 알고리즘 정확도 : {self.get_accuracy(this, k_fold)}')

    @staticmethod
    def get_accuracy(this, k_fold) -> object:
        score = cross_val_score(RandomForestClassifier(), this.train, this.label, 
                                cv=k_fold, n_jobs=1, scoring='accuracy')
        return round(np.mean(score)*100, 2)