

class Contract:

    def __init__(self, name, phone) -> None:
        self.name = name
        self.phone = phone

    def __str__(self) -> str:
        return f'이름 : {self.name}' \
               f'전화번호 : {self.phone}'
    
    @staticmethod
    def create_user(members:dict):
        name = input('이름 입력: ').title()
        phone = input('전화번호 입력 : ')
        members[name] = phone
        this = Contract(name, phone).__dict__
        print('----------')
        print(f'*****{name} 입력 완료*****')
        print(f'*****{phone} 입력 완료*****')
        print('----------')
        members.update(this)
        return members
    
    def find_name(self):
        name = input('검색할 이름 입력: ').title()
        phone = members.get(name, '존재하지 않습니다.')
        print('----------')
        print(f'{name}:', phone)
        print('----------')

    def modify_name(self):
        name = input('수정할 이름 입력: ').title()
        if name not in members.keys(): # members.keys(): key만 추출하기
            print('----------')
            print(f'{name} 회원은 존재하지 않습니다.')
            print('----------')
        else:
            phone = input('새로운 전화번호 입력: ')
            members[name] = phone
            print('----------')
            print(f"*****{name} 수정 완료*****")
            print(f'{name}:', phone)
            print('----------')
        return members
    
    def delete_user(self):
        name = input('삭제할 이름 입력: ').title()
        if name not in members.keys():
            print('----------')
            print(f'{name} 회원은 존재하지 않습니다.')
            print('----------')
        else:
            ask = input(f"{name} 회원을 정말로 삭제할까요?(y/n): ").lower()
            if ask == 'y':
                del members[name]
                print('----------')
                print(f"*****{name} 삭제 완료*****")
                print('----------')
            else:
                print('----------')
                print(f'{name} 회원을 삭제하지 않았습니다.')
                print('----------')
            return members

    def user_list(self):
        print('----------')
        for k, v in members.items(): # members.items(): key, value 추출하기
            print(f'{k}: {v}')
        print('----------')

    def exit(self):
        print('----------')
        print('프로그램을 종료합니다.')
        print('----------')

if __name__ == "__main__":
    members = {}
    while True:
        menu = input('회원정보 추가(a), 검색(f), 수정(u), 삭제(d), 목록(s), 종료(x): ')
        if menu=='a':
            Contract.create_user(members)
        elif menu=='f':
            Contract.find_name(members)
        elif menu=='u':
            Contract.modify_name(members)
        elif menu=='d':
            Contract.delete_user(members)
        elif menu=='s':
            Contract.user_list(members)
        elif menu=='x':
            Contract.exit()
            break # loop 끝내기