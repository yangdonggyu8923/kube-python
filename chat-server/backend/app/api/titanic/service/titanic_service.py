
from app.api.titanic.model.titanic_model import TitanicModel
import pandas as pd


class TitanicService:

    model = TitanicModel() 

    def process(self): # 테스트 모델
        print(f'프로세스 시작')
        this = self.model   # this = property, self = 자기 자신
        this.train = self.new_model('train.csv') # model의 필드명과 동일하게 = this.필드명
        this.test = self.new_model('test.csv')
        self.df_info(this)
        this.id = this.test['PassengerId']

        self.drop_feature(this, 'Ticket', 'SibSp', 'Name', 'Parch', 'Cabin' )
        self.df_info(this)

        this = self.create_train(this)
        

    def new_model(self, playload) -> object:
        this = self.model
        this.context = './app/api/titanic/data/'
        this.fname = playload
        return pd.read_csv(this.context + this.fname)
        

    @staticmethod
    def create_train(this) -> str:  # 훈련 세트
        return this.train.drop('Survived', axis=1) # 0 : 행, 1 : 열 -> 그러므로 해당 라인의 axis에는 열을 주었음

    @staticmethod
    def create_label(this) -> str:  # 답
        return this.train['Survived']
    
    @staticmethod
    def drop_feature(this, *feature) -> object:
        
        # for i in feature:
        #     this.train = this.train.drop([i], axis=1)
        #     this.test = this.test.drop([i], axis=1)
        
        # for i in [this.train, this.test]:
        #     for j in feature:
        #         i.drop(j, axis=1, inplace=True)

        [i.drop(j, axis=1, inplace=True) for j in feature for i in [this.train, this.test]]

        return this
    
    @staticmethod
    def df_info(this):
        # for i in [this.train, this.test]:
        #     print(f'{i.info()}')    # head는 앞에서 5개, tail은 뒤에서 5개 항목을 보여줌
            

        [i.info() for i in [this.train, this.test]]