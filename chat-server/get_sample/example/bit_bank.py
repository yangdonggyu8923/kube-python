import random


class BitBank:
    
    def __init__(self) -> None:
        '''
        [요구사항(RFP)]
        은행이름은 비트은행이다.
        입금자 이름(name), 계좌번호(account_number), 금액(money) 속성값으로 계좌를 생성한다.
        계좌번호는 3자리-2자리-6자리 형태로 랜덤하게 생성된다.
        예를들면 123-12-123456 이다.
        금액은 100 ~ 999 사이로 랜덤하게 입금된다. (단위는 만단위로 암묵적으로 판단한다)
        '''
        self.bank_name = "비트은행"
        self.name = "홍길동"
        self.ac_num1 = random.randint(100, 999)
        self.ac_num2 = random.randint(10, 99)
        self.ac_num3 = random.randint(100000, 999999)
        self.money = random.randint(100, 999)
        self.a = f'은행명: {self.bank_name}, 이름: {self.name}, 계좌번호: {self.ac_num1}-{self.ac_num2}-{self.ac_num3}, 금액: {self.money}'
        print(self.a)
    
       
    

