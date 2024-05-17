from example.utils import myRandom


class LeapYear:

    def __init__(self) -> None:
        print(f'utils.py myRandom() 를 이용하여 윤년계산기 객체를 생성합니다')
        print ('(ex) 2020년은 윤년입니다. 단 컴프리헨션을 사용합니다')

    def is_leap_year(self, year):
        y= myRandom(2000, 2024)
        
        # 자바 스타일 = String s1 or s2 = () ? "윤년" : "평년"
        # 자바 스타일 = String s = () ? () ? T : F : F;
        s1 = '윤년' if ( y % 4 == 0 and y % 100 != 0 ) else '평년'
        s2 = '윤년' if ( y % 400 == 0 ) else '평년'
        s = '윤년' if ( y % 4 == 0 and y % 100 != 0 ) or y % 400 == 0 else '평년'
        print(f'{y}년은 {s}입니다.')