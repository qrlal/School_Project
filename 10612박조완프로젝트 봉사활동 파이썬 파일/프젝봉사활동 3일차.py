def f(x):
    print(x**2+1)

f(1) # 2출력. 수학에서의 함수와 비슷한 개념

# 현재 초를 이용해서 난수생성함수 만들어봐
import datetime
def random(a) :
    time = datetime.datetime.now().second
    return time %(a+1)

print(random(10)) #0~10사이 무작위 수 가져오는 함수