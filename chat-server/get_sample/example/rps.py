import random


class RPS:

    def __init__(self) -> None:
        print(f'utils.py myRandom() 를 이용하여 가위바위보 객체를 생성합니다')

    def myRandom(start, end): return random.randint(start, end-1)
    if __name__ == "__main__":
        c = myRandom(1,4)
        a = input('1, 2, 3:')
        # 가위 : 1, 바위 : 2, 보 : 3
        if a == '1':
            p = '가위'
        elif a == '2':
            p = '바위'
        else:
            p = '보'
        
        rps = ['가위', '바위', '보']
        if p == rps[c-1]:
            print(f'컴 : {rps[c-1]}, 당신: {p}, 비겼습니다' )
        elif p == rps[c%3]:
            print(f'컴 : {rps[c-1]}, 당신: {p}, 이겼습니다' )
        else:
            print(f'컴 : {rps[c-1]}, 당신: {p}, 졌습니다' )