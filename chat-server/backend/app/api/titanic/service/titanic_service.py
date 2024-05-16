
from app.api.titanic.model.titanic_model import TitanicModel
import pandas as pd


class TitanicService:

    model = TitanicModel() 

    def preprocess(self): # 머신러닝 후처리
        print(f'전처리 시작')
        self.model.preprocess('app/api/context/data/train.csv', 'app/api/context/data/test.csv')
        # this = property, self = 자기 자신


    def modeling(self):
        print(f'모델링 시작')
        this = self.model
        
    def learning(self):
        print(f'학습 시작')
        print(f'결정트리를 활용한 검증 정확도 : ')
        print(f'랜덤포레스트를 활용한 검증 정확도 : ')
        print(f'나이브베이즈를 활용한 검증 정확도 : ')
        print(f'KNN를 활용한 검증 정확도 : ')
        print(f'SVM를 활용한 검증 정확도 : ')
        this = self.model

    def postprocess(self):
        print(f'후처리 시작')
        this = self.model

    def submit(self):
        print(f'제출 시작')
        this = self.model

        

    # @staticmethod
    # def create_train(this) -> str:  # 훈련 세트
    #     return this.train.drop('Survived', axis=1) # 0 : 행, 1 : 열 -> 그러므로 해당 라인의 axis에는 열을 주었음

    # @staticmethod
    # def create_label(this) -> str:  # 답
    #     return this.train['Survived']
    
    
    
    # @staticmethod
    # def df_info(this):
    #     # for i in [this.train, this.test]:
    #     #     print(f'{i.info()}')    # head는 앞에서 5개, tail은 뒤에서 5개 항목을 보여줌
            

    #     [print(f'{i.info()}') for i in [this.train, this.test]]


    # @staticmethod
    # def pclass_ordinal(this) -> object:
    #     return this
    
    # @staticmethod
    # def name_nominal(this) -> object:
    #     return this
    
    # @staticmethod
    # def extract_title_from_name(this) -> object:
    #     combine = [this.train, this.test]
    #     for i in combine:
    #         i['Title'] = i['Name'].str.extract('([A-Za-z]+)\.')
    #     return this

    # @staticmethod
    # def sex_nominal(this) -> object:
    #     return this
    
    # @staticmethod
    # def age_ratio(this) -> object:
    #     return this
    
    # @staticmethod
    # def fare_ratio(this) -> object:
    #     return this
    
    # @staticmethod
    # def embarked_nominal(this) -> object:
    #     return this
    
    # ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 
    #  'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked']