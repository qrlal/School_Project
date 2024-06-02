mlist = [1, 2, 3, 4]
mlist[0] # 1
mlist[1] # 2
mlist[2] # 3

# while True :
#     print("hi")

# a = 0
# while a < 10 :
#     print("bye")

# *
# **
# ***
# ****
# *
# **
# ***
# ****
# 이게 무한 출력되는 코드 만들어봐. list하고 whlie이용해서

mlist = ["*","**","***","****"]

a = 0
while True :
    print(mlist[a%4])
    a += 1