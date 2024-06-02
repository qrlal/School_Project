import random

a = random.randint(1,100)
b = random.randrange(1,100)

mlist = [1,2,3,4]
print(len(mlist)) #길이

mlist = [1,3,2,4]
mlist.sort() #정렬
print(mlist)

mlist = [1,2,3,4]
random.shuffle(mlist) #섞기 
print(mlist)

c = random.choices(mlist) #고르기
print(c)