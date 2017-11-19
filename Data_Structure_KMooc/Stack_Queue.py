# Stack: 쌓음. Last In First Out(LIFO), 나중에 넣은 데이터가 먼저 반환하도록 설계됨
# Data의 입력을 Push, 출력을 Pop이라고 함
# 파이썬은 list.append(), list.pop()으로 Stack 구조를 활용
listex= [1,2,3,4,5]
listex.append(6)
listex.append(7)

for _ in range(len(listex)):
    print(listex.pop())

# Queue: 줄을 서다. First in First Out(FIFO), 먼저 넣은 데이터가 먼저 반환되도록 설계됨
# Data의 입력을 Put, 출력을 Get으로 이해함
# 파이썬은 list.append(), list.pop(0)으로 Queue 구조를 활용

listex= [1,2,3,4,5,6,7]
for _ in range(len(listex)):
    print(listex.pop(0))
