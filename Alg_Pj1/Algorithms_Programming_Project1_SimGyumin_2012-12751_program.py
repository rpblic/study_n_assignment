import random
import copy
import numpy
# import time
# from matplotlib.pyplot import *
###Variables##############################################################
n= 128
sort_num= 0
iter_num= 1000
ordered_list= [i for i in range(n)]
unordered_list= copy.deepcopy(ordered_list)
sigma_operation= 0


###Tool Functions##########################################################
def get_unordered():
    global sort_num
    random.shuffle(unordered_list)
    sort_num += 1
    return unordered_list

def Statistic_iter(func, iter_num, l, u):
    global sigma_operation
    op_list= []
    for i in range(iter_num):
        sigma_operation= 0
        (S, op)= func(get_unordered(), l, u)
        if S != ordered_list:
            raise ValueError('Not ordered correctly')
        op_list.append(sigma_operation)
    max_op= max(op_list)
    min_op= min(op_list)
    average_op= numpy.mean(op_list)
    var_op= numpy.var(op_list)
    return (func.__name__, iter_num, min_op, average_op, max_op, var_op)

###Sorting Functions#######################################################
def part(S, l, u):
    pivot_val= S[l]
    i= l+1
    j= u
    op= 0
    while i<=j:
        while i<=u and S[i] <= pivot_val:
            i+= 1
            op+= 1
        if i<=u: op+= 1
        while i<=j and S[j] > pivot_val:
            j-= 1
            op+= 1
        if i<=j: op+= 1
        if i<j:
            S[i], S[j]= S[j], S[i]
            #Possible in Python!
            i+= 1
            j-= 1
    S[l], S[j]= S[j], S[l]
    return (j, op)

def QuickS_1(S, l, u):
    global sigma_operation
    if l<u:
        (p, op)= part(S,l,u)
        sigma_operation+= op
        QuickS_1(S,l,p-1)
        QuickS_1(S,p+1,u)
    return (S, sigma_operation)
    # might be B(128)= 769, W(128)= 8128

def QuickS_M3(S, l, u):
    global sigma_operation
    m= int((l+u)/2)
    if l<u:
        if S[l]>S[m]:
            S[l], S[m]= S[m], S[l]
        sigma_operation+= 1
        if S[m]>S[u]:
            S[m], S[u]= S[u], S[m]
            if S[l]>S[m]:
                S[l], S[m]= S[m], S[l]
            sigma_operation+= 1
        sigma_operation+= 1
        S[l+1], S[m]= S[m], S[l+1]
        (p, op)= part(S,l+1,u-1)
        sigma_operation+= op
        QuickS_M3(S,l,p-1)
        QuickS_M3(S,p+1,u)
    return (S, sigma_operation)

def InsertionS(S, l, u):
    if l<u:
        return insert(InsertionS(S,l,u-1), l, u)
    elif l==u:
        return S
    else: raise Exception('Something went wrong.')

def insert(S, l, u):
    global sigma_operation
    for i in range(u-1, l-1, -1):
        sigma_operation+= 1
        if S[i]> S[i+1]:
            S[i], S[i+1]= S[i+1], S[i]
        else:
            return S
    return S

def QuickS_Insertion_added(S, l, u):
    global  sigma_operation
    m= int((l+u)/2)
    if u-l+1>= 9:
        if S[l]>S[m]:
            S[l], S[m]= S[m], S[l]
        sigma_operation+= 1
        if S[m]>S[u]:
            S[m], S[u]= S[u], S[m]
            if S[l]>S[m]:
                S[l], S[m]= S[m], S[l]
            sigma_operation+= 1
        sigma_operation+= 1
        S[l+1], S[m]= S[m], S[l+1]
        (p, op)= part(S,l+1,u-1)
        sigma_operation+= op
        QuickS_Insertion_added(S,l,p-1)
        QuickS_Insertion_added(S,p+1,u)
    else:
        S= InsertionS(S, l, u)
    return (S, sigma_operation)

###QuickS_1   #############################################################
print(QuickS_1(ordered_list, 0, n-1))   # result: 8255
sigma_operation= 0
print(QuickS_1([7,0,2,1,5,4,6,3,11,8,10,9,13,12,14,15], 0, 15))     # result: 46
print(Statistic_iter(QuickS_1, iter_num, 0, n-1))
# ('QuickS_1', 1000, 775, 942.19000000000005, 1312, 5558.3419000000004)


###QuickS_M3   ############################################################
print(QuickS_M3([i for i in range(16)], 0, 15))    # result: 43
sigma_operation= 0
print(QuickS_M3([2,12,4,10,6,14,8,1,3,5,7,9,11,13,15,0], 0, 15))    # result: 80
print(Statistic_iter(QuickS_M3, iter_num, 0, n-1))
# ('QuickS_M3', 1000, 760, 842.202, 1001, 1495.6011960000001)


###QuickS_Insertion_added   ###############################################
print(QuickS_Insertion_added([i for i in range(16)], 0, 15))    # result: 43
sigma_operation= 0
print(QuickS_Insertion_added([2,13,4,15,6,14,8,1,3,5,7,12,11,10,9,0], 0, 15))    # result: 80
print(Statistic_iter(QuickS_Insertion_added, iter_num, 0, n-1))
# ('QuickS_Insertion_added', 1000, 738, 827.70399999999995, 1020, 1861.5623840000001)
