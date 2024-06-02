import random

mlist = ["a","b","c","d","e","f"] #원하는 단어 입력

while True :
    a = random.choice(mlist)
    print(a)
    result = input()

    if result != a :
        while True :
                print("오답")
                print("------------")
                print(a)
                result = input()
                
                if result == a :
                    print("정답")
                    print("------------")
                    break

    else :
        print("정답")
        print("------------")