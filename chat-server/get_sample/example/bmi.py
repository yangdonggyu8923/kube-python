from example.utils import Member


class BMI():
    def __init__(self) -> None:
        '''utils.py / Members(), myRandom() 를 이용하여 BMI 지수를 구하는 계산기를 작성합니다.'''

    def getBMI(self, height, weight):
        '''BMI 지수를 계산합니다'''
        this = Member()
        this.name = '홍길동'
        this.height = 170.8
        this.weight = 80.5
        res = this.weight / this.height**2 * 10000

        if res > 25:
            return f'{this.name}님은 비만입니다.'