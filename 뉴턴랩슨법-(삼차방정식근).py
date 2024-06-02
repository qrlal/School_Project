import math

def f(x):
    return a*x**3 + b*x**2 + c*x + d

def f_p(x):
    return 3*a*x**2 + 2*b*x + c #미분한거

def newton_raphson(a, b, c, d, x0, min=1/(10**8), max_ite=300):    # min=1/(10**8): 근 사이의 차이가 0.00000001
    x = x0
    ite = 0

    while abs(f(x)) > min and ite < max_ite:
        x = x - f(x) / f_p(x)
        ite += 1

    if ite == max_ite:
        print("최대 반복 횟수에 도달. 근을 찾지 못했습니다.")
    else:
        print("근1:", round(x, 2))
        return round(x, 2)
    
def f_2(x):
    return a*x**2 + (a*d_2+b)*x +  d_2*(a*d_2+b)+c #조립제법 이용해서 나머지 이차식 구함

# 입력 받기
a = float(input("a 값을 입력하세요: "))
b = float(input("b 값을 입력하세요: "))
c = float(input("c 값을 입력하세요: "))
d = float(input("d 값을 입력하세요: "))
x0 = float(input("초기 추정값 x0을 입력하세요: "))

# 뉴턴-랩슨법으로 근 찾기
d_2 = newton_raphson(a, b, c, d, x0)

# 이차방정식의 계수들 
a_ = a
b_ = a*d_2+b
c_ = d_2*(a*d_2+b)+c


def quadratic_formula(a_, b_, c_): # 이차방정식의 근의 공식
    discriminant = b_**2 - 4*a_*c_ # 판별식 

    if discriminant >= 0:
        root1 = (-b_ + math.sqrt(discriminant)) / (2*a_)
        root2 = (-b_ - math.sqrt(discriminant)) / (2*a_)
        print("근2:", root1)
        print("근3:", root2)
    else:
        real_part = -b_ / (2*a_)
        imagin_part = math.sqrt(-discriminant) / (2*a_)
        root1 = complex(real_part, imagin_part)
        root2 = complex(real_part, -imagin_part)
        print("근2:", root1)
        print("근3:", root2)

quadratic_formula(a_, b_, c_)

# 1번째 (x-1)^3              1, -3, 3, -1
# 2번째 (x-1)(x-2)(x-3)      1, -6, 11, -6
# 3번쨰 (x-101)(x-20)(x-39)  1, -160, 6739, -78780
# 4번째 (x-1)(x^2+x+1)       1, 0, 0, -1   허근 포함.   0.8660254037844386 ~= 루트(3)/2