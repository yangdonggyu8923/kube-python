
from app.api.titanic.model.titanic_model import TitanicModel
import pandas as pd


class TitanicService:

    model = TitanicModel() 

    def process(self): # 테스트 모델
        print(f'프로세스 시작')
        this = self.model   # this = property, self = 자기 자신
        feature = ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked']
        this.train = self.new_model('train.csv') # model의 필드명과 동일하게 = this.필드명
        this.test = self.new_model('test.csv')
        self.df_info(this)
        this.id = this.test['PassengerId']

        this = self.name_nominal(this)
        self.df_info(this)
        # self.drop_feature(this, 'Ticket', 'SibSp', 'Name', 'Parch', 'Cabin' )
        self.df_info(this)

        this = self.embarked_nominal(this)
        this = self.age_ratio(this)
        this = self.fare_ratio(this)
        this = self.pclass_ordinal(this)
        this = self.sex_nominal(this)

        self.df_info(this)

        this = self.create_train(this)
        


        

    @staticmethod
    def create_train(this) -> str:  # 훈련 세트
        return this.train.drop('Survived', axis=1) # 0 : 행, 1 : 열 -> 그러므로 해당 라인의 axis에는 열을 주었음

    @staticmethod
    def create_label(this) -> str:  # 답
        return this.train['Survived']
    
    
    
    @staticmethod
    def df_info(this):
        # for i in [this.train, this.test]:
        #     print(f'{i.info()}')    # head는 앞에서 5개, tail은 뒤에서 5개 항목을 보여줌
            

        [print(f'{i.info()}') for i in [this.train, this.test]]


    @staticmethod
    def pclass_ordinal(this) -> object:
        return this
    
    @staticmethod
    def name_nominal(this) -> object:
        return this
    
    @staticmethod
    def extract_title_from_name(this) -> object:
        combine = [this.train, this.test]
        for i in combine:
            i['Title'] = i['Name'].str.extract('([A-Za-z]+)\.')
        return this

    @staticmethod
    def sex_nominal(this) -> object:
        return this
    
    @staticmethod
    def age_ratio(this) -> object:
        return this
    
    @staticmethod
    def fare_ratio(this) -> object:
        return this
    
    @staticmethod
    def embarked_nominal(this) -> object:
        return this
    
    # ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 
    #  'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked']