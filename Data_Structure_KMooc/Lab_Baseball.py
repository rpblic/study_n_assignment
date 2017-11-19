import random

# __init__: get random answer number
# ans: get 3-numbered answer number, with no repitition
# input: get input number
# num_check: check whether input is int, 100<=input<1000, and has no repitition
# strike_check: check whether input number has strikes
# ball_check: check whether input numper has balls
# homerun: end program when input number has 3 strikes

def list_number(inp):
    inp100= inp//100
    inp10= (inp-100*inp100)//10
    inp1= (inp-100*inp100-10*inp10)
    return [inp100, inp10, inp1]

def num_check(inp):
    try:
        inp_num= int(inp)  #1 check whether is int
        # print(100<=inp<1000); print(len(set_number(inp))==3)
        return 100<=inp_num<1000 and len(set(list_number(inp_num)))==3
        #&, |는 set의 연산자이다. 논리 연산자는 and, or
    except:
        return False

def strike_check(inp):
    result= 0
    for i, num in enumerate(list_number(inp)):
        if list_number(ans)[i]==num: result +=1
    return result

def ball_check(inp):
    return len(set(list_number(inp)) & set(list_number(ans))) - strike_check(inp)

# ans= 731
# print(strike_check(731))
# print(ball_check(327))
# print(num_check("string"))

homerun= False
ans= 0
while not num_check(ans):
    ans= random.randrange(100, 1000)
# print("Test: Answer is {}".format(ans))
while not homerun:
    inp_num= input("Input your number.\t")
    if num_check(inp_num): #Boolean is True then
        inp_num= int(inp_num)
        strike= strike_check(inp_num)   #int 0~3
        if strike ==3:  #Homerun then
            homerun= True
            print("Got it! Homerun")
            if input("Continue?")=="Y" :    #want to repeat then
                homerun= False
                ans= random.randrange(100, 1000)
                while not num_check(ans):
                    ans= random.randrange(100, 1000)
        else:   #Not Homerun then
            ball= ball_check(inp_num) #int 0~3
            print(strike, ball)
    else: print("Error: Check that you input right number.")  #Boolean is False then
