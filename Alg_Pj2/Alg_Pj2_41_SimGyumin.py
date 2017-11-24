"""
Abstract(read it first):
You can run this file with only write 'python Alg_Pj2_41_SimGyumin.py (the name of input file) (the name of output file)'.
Then this program will automatically check the input file, run the codes, and make the output txt file.

But as this program contains both algorithms and analysis functions, it takes too many computing time.
(In my computer, it takes 25 minutes to compute all cases of analysis.)
You could avoid this analysis functions to run; you could do this by write command
'python Alg_Pj2_41_SimGyumin.py (the name of input file) (the name of output file) analyze:0'.
Then this file checks the argv of command and turn of the running of analysis function.
Also you could turn off the overall comments to be shown(just write the results in output txt file.)
by adding argv 'add_comment:0'.
Or you could turn off writing the output file and just print it in command interpreter
by adding argv 'write_txt:0'.
"""

# Module #######################################################################
import os, sys, random
import numpy as np
import copy
import queue
import matplotlib.pyplot as plt
os.chdir(os.getcwd())
# I/O ##########################################################################
def list_sort(profit_list, weight_list):
    """
    Take inputs the list of profits and weights of objects, and rearrange it to sort by
    (profit/weight) in decreasing order.
    """
    p_w_list=[]
    sorted_profit_list=[]
    sorted_weight_list=[]
    for profit, weight in zip(profit_list, weight_list):
        p_w_list.append(profit/weight)
    sorted_list= sorted(p_w_list, reverse=True)
    for i, val in enumerate(sorted_list):
        j= p_w_list.index(val)
        sorted_profit_list.append(profit_list[j])
        sorted_weight_list.append(weight_list[j])
    return (sorted_list, sorted_profit_list, sorted_weight_list)

def opener(inputfile='input.txt', delimiter=','):
    """
    open txt file and return N, MAXWEIGHT, list of profit, list of weight.
    txt file must be in this form:
    N MAXWEIGHT
    (profit of object1) (weight of object1)
    (profit of object2) (weight of object2)
    (profit of object3) (weight of object3)
    ...
    """
    if len(sys.argv)>1:
        inputfile= sys.argv[1]
    weight_list= []
    profit_list= []
    if os.path.isfile(inputfile):
        with open(inputfile, 'rt') as f:
            firstline= f.readline()
            N, MAXWEIGHT= firstline.split(delimiter)
            N, MAXWEIGHT= int(N), int(MAXWEIGHT)
            lines= f.readlines()
            for line in lines:
                line= line[:-1]     #deleting \n
                line= line.split(delimiter)
                line= list(map(int, line))
                profit_list.append(line[0])
                weight_list.append(line[1])
    else: raise IOError
    p_w_list, profit_list, weight_list= list_sort(profit_list, weight_list)
    return (N, MAXWEIGHT, profit_list, weight_list)

def writer(profit_list, weight_list, max_knapsack_array= [0,0,0,0,0], comment='', \
            max_profit= 0, outputfile='output.txt', delimiter=',\t'):
    """
    write txt file such that includes those informations:
    list of objects, comments of algorithm if necessary, max profit, weight of
    result.
    """
    if len(sys.argv)>2:
        outputfile= sys.argv[2]
    with open(outputfile, 'at') as f:
        if comment:
            comment= comment+ '\n\n'
            f.write(comment)
        # print(list(max_knapsack_array))
        string_line= '{},\t{}\n'.format(max_profit, list(max_knapsack_array))
        f.write(string_line)
        for line in list(zip(profit_list, weight_list, max_knapsack_array)):
            line= list(map(str, line))
            string_line= delimiter.join(line)+'\n'
            f.write(string_line)

def GetItemList(q):
    """
    To see the items in Queue, get out all items of queue, put it in python list and print the list.
    And then put all elements in a list to the queue in the same way.
    """
    ret=[]
    elmts=[]
    n=q.qsize()
    while n > 0:
        elmt= q.get()
        elmts.append(elmt)
        i= elmt[1]['i']
        ret.append({'node': (i, max(int(elmt[1]['knapsack_array'][i-1]), 0)),\
                    'knapsack_array': elmt[1]['knapsack_array'], 'Tprofit': elmt[1]['Tprofit']})
        n -= 1
    for item in elmts:
        q.put(item)
    if q.qsize()== len(ret): return ret
    else: return IOError

# Setting ######################################################################
(N, MAXWEIGHT, profit_list, weight_list)= opener('input.txt', ' ')
# open file if there are no input value of filename.

#global variables
max_profit= 0
max_knapsack_array= np.zeros(N)
comment= str()
operation_num= 0

# Algorithm Function ###########################################################
"""
Abstract of algorithm:
I've write three algorithm with python; DP, BT and BB.
Code is similar with pseudo-code learned from class, but it differs in two ways.
First, there are global variable 'comment', and in every major trace of algorithm there are comments of
what trace the algorithm goes through. It is writen by comment += (any comments) or if add_comment: comment += (any comments).
Second, there are global variable 'operation_num' to check the number of operation.
For the case of BT and BB, I hypothesize that the comparison shown in each pseudo-code can be an operation.
But I didn't hypothesize that computing the value is the operation: hence, in BT, operation_num variable checks
the Promising sub-algorithm(for comparison) as operation, but not checking the function for
computing the upper bound(function Bd) as operation.

*Note1: in pseudo-code it is shown that the algorithm is recursing BackTracking Algorithm itself, but I've
made inner-function i_th_check, for making the inputs of all algorithms same. In that way, I can run the functions
for analysis with good way.
**Note2: I often use copy.deepcopy. This is because of the character of python's soft-copy reference system.
copy.deepcopy makes the deep copy of the data.
"""

def DP_K(N, MAXWEIGHT, profit_list, weight_list, add_comment= True):
    """
    0/1 knapsack problem with DynamicProgramming Algorithm.
    Input:
    N: the number of objects. It must be same with the length of profit_list and weight_list.
    MAXWEIGHT: the capacity of knapsack. It is given in input txt file.
    profit_list, weight_list: the lists of profit and weight of objects. It also is given by
                            input txt file, and opener() function make data into two lists.
    add_comment: (optional) make comments for check the traces the algorithm takes.
                It will be writen in interpreter and output file.
    Output:
    knapsack_array: the list of knapsack. We could check what object has been inserted to knapsack.
    totalprofit_array[N, MAXWEIGHT]: totalprofit_array is same with the table we draw in class.
    The algorithm returns only maximum value of profit. But we could check the whole array in comment.
    """
    global comment, operation_num
    comment= str()
    operation_num= 0
    comment += '\nDynamicProgramming-----------------------------------------------------------------------------\n\n'
    totalprofit_array= np.zeros((N+1, MAXWEIGHT+1))        #0 to MAXWEIGHT
    # for j in range(MAXWEIGHT+1): totalprofit_array[0,j]= 0
    # Must be done since it is a base case, but can be omitted as I set the base case(totalprofit) as zeros array.
    zero_one_array= np.zeros((N+1, MAXWEIGHT+1))
    for i in range(1, N+1):     #except case i=0
        for k in range(MAXWEIGHT+1):
            if k< weight_list[i-1]:
                totalprofit_array[i,k]= totalprofit_array[i-1, k]
            elif totalprofit_array[i-1,k] < totalprofit_array[i-1, k-weight_list[i-1]]+profit_list[i-1]:
                zero_one_array[i,k]= 1
                totalprofit_array[i,k]= totalprofit_array[i-1, k-weight_list[i-1]]+profit_list[i-1]
            else:
                totalprofit_array[i,k]= totalprofit_array[i-1,k]
            operation_num +=1
                # It could be also written as:
                # totalprofit_array[i,k]= max(totalprofit_array[i-1,k],\
                #                             totalprofit_array[i-1, k-weight_list[i-1]]+profit_list[i-1])
                # But I programmed to make zero_one_array
                # to find out whether I've included the object in a knapsack.
                #
                # Code below is how I've find out what object to choose.
    estimator= 0
    knapsack_array= np.zeros(N)
    for t in range(N, 0, -1):
        knapsack_array[t-1]= zero_one_array[t, (MAXWEIGHT-estimator)]
        if zero_one_array[t, (MAXWEIGHT-estimator)]== 1:
            estimator+= weight_list[t-1]
    if add_comment:
        comment+= 'The array of profit is:\n'+ str(totalprofit_array)+'\n'
        comment+= 'The array of knapsack is: '+ str(knapsack_array)+ '\n'
        comment+= '######## The number of operation is: '+ str(operation_num) + '\n'
    return (knapsack_array, totalprofit_array[N, MAXWEIGHT])

def Bd(i, Tprofit, Tweight, N, MAXWEIGHT, profit_list, weight_list):
    """
    Sub-algorithm Bd for compute the upper bound.
    Input:
    i: the level of node.
    Tprofit: Total profit of node.
    Tweight: Total weight of node.
    N: the number of objects. It must be same with the length of profit_list and weight_list.
    MAXWEIGHT: the capacity of knapsack. It is given in input txt file.
    profit_list, weight_list: the lists of profit and weight of objects. It also is given by
                            input txt file, and opener() function make data into two lists.
    Output:
    Ubound: the upper bound of node.

    *Note: When Total weight is bigger than MAXWEIGHT, it returns Ubound= False.
            In BT_K algorithm, it is considered as nonpromising situation.
    """
    global max_profit, max_knapsack_array
    if Tweight> MAXWEIGHT:
        return False
    j= i+1
    Ubound= Tprofit
    Lim_weight= Tweight
    while j<= N and Lim_weight+ weight_list[j-1] <= MAXWEIGHT:
        Lim_weight += weight_list[j-1]
        Ubound += profit_list[j-1]
        j += 1
    if j<=N:
        Ubound += (MAXWEIGHT - Lim_weight)*(profit_list[j-1]/weight_list[j-1])
    return Ubound

def Promising(i, Tprofit, Tweight, N, MAXWEIGHT, profit_list, weight_list):
    """
    Sub-algorithm Promising for decide which this node is promising.
    Input:
    i: the level of node.
    Tprofit: Total profit of node.
    Tweight: Total weight of node.
    N: the number of objects. It must be same with the length of profit_list and weight_list.
    MAXWEIGHT: the capacity of knapsack. It is given in input txt file.
    profit_list, weight_list: the lists of profit and weight of objects. It also is given by
                            input txt file, and opener() function make data into two lists.
    Output:
    True or False Boolean value.
    """
    global max_profit, operation_num
    operation_num += 1
    if Tweight>= MAXWEIGHT:
        return False
    else:
        bound= Bd(i, Tprofit, Tweight, N, MAXWEIGHT, profit_list, weight_list)
        return (bound> max_profit)

def BT_K(N, MAXWEIGHT, profit_list, weight_list, add_comment= True):
    """
    0/1 knapsack problem with BackTracking Algorithm.
    Input:
    N: the number of objects. It must be same with the length of profit_list and weight_list.
    MAXWEIGHT: the capacity of knapsack. It is given in input txt file.
    profit_list, weight_list: the lists of profit and weight of objects. It also is given by
                            input txt file, and opener() function make data into two lists.
    add_comment: (optional) make comments for check the traces the algorithm takes.
                It will be writen in interpreter and output file.
    Output:
    max_knapsack_array: the list of knapsack with maximum profit.
    max_profit: value of maximum profit.(integer)
    """
    global max_profit, max_knapsack_array
    global comment, operation_num
    # Initialize variable again, and start with the base case
    max_profit= 0
    max_knapsack_array= np.zeros(N)
    comment= str()
    operation_num= 0
    comment += '\nBackTracking-----------------------------------------------------------------------------\n\n'
    if add_comment:
        comment += 'i\t\t'+ 'Total-Profit\t'+ 'Total-Weight\t'+ 'Array-of-knapsack\t\t'+ 'Max-Profit\t'+ 'Max-knapsack-array\n'
        comment += '_____________________________________________________________________________________\n'
    def i_th_check(i, knapsack_array, Tprofit, Tweight, add_comment= True):
        global max_profit, max_knapsack_array
        global comment, operation_num
        if add_comment:
            comment += str(i)+ '\t\t'+ str(Tprofit)+ '\t\t'+ str(Tweight)+ '\t\t'+\
                        str(knapsack_array)+ '\t\t'+ str(max_profit)+ '\t\t'+ str(max_knapsack_array)+ '\n'
        operation_num += 1
        if Tweight <= MAXWEIGHT and Tprofit > max_profit: #Changing Maximum Value(profit, max_knapsack_array)
            max_profit= copy.deepcopy(Tprofit)
            max_knapsack_array= copy.deepcopy(knapsack_array)
            if add_comment:
                comment += '\tMaxProfit array changed: '+ str(max_knapsack_array)+\
                            '\tmax_profit: '+ str(max_profit)+ '\n'
        else:           #Do not changing the Maximum Value.
            if add_comment: comment+= '\tMaxProfit do not changed.\n'
        if Promising(i, Tprofit, Tweight, N, MAXWEIGHT, profit_list, weight_list):
            if add_comment:
                comment+= '\tPromising('+ str(Bd(i, Tprofit, Tweight, N, MAXWEIGHT, profit_list, weight_list))+\
                            ' > '+ str(max_profit) +'): split two children nodes\n'
            #Promising: Check the Left node.
            knapsack_array[i]= 1
            i_th_check(i+1, knapsack_array, Tprofit+profit_list[i], \
                        Tweight+weight_list[i], add_comment= add_comment)
            #Promising: Check the Right node.
            knapsack_array[i]= 0
            i_th_check(i+1, knapsack_array, Tprofit, Tweight, add_comment= add_comment)
        else:   #Not Promising.
            bound= Bd(i, Tprofit, Tweight, N, MAXWEIGHT, profit_list, weight_list)
            if bound: #When upper bound is smaller than Maximum profit.
                if add_comment:
                    comment+= '\tNot Promising('+ str(Bd(i, Tprofit, Tweight, N, MAXWEIGHT, profit_list, weight_list))+\
                                ' <= '+ str(max_profit) +'): pass the children nodes\n'
            else: # When the sum of weights exceeds MAXWEIGHT.
                if add_comment: comment += '\tNot Promising(weight exceeded): pass the children nodes\n'
        return (max_knapsack_array, max_profit)
    result= i_th_check(0, np.zeros(N), 0, 0, add_comment= add_comment) # The base case of recursive call.
    if add_comment:
        comment+= 'Result MaxProfit array: '+ str(result[0])+ ',\tmax_profit: '+ str(result[1])+ '\n'
        comment+= '######## The number of operation is: '+ str(operation_num) + '\n'
    return result

def BB_K(N, MAXWEIGHT, profit_list, weight_list, add_comment= True):
    """
    0/1 knapsack problem with BackTracking Algorithm.
    Input:
    N: the number of objects. It must be same with the length of profit_list and weight_list.
    MAXWEIGHT: the capacity of knapsack. It is given in input txt file.
    profit_list, weight_list: the lists of profit and weight of objects. It also is given by
                            input txt file, and opener() function make data into two lists.
    add_comment: (optional) make comments for check the traces the algorithm takes.
                It will be writen in interpreter and output file.
    Output:
    max_knapsack_array: the list of knapsack with maximum profit.
    max_profit: value of maximum profit.(integer)
    """
    global max_profit, max_knapsack_array
    global comment, operation_num
    # Initialize variable again
    max_profit= 0
    max_knapsack_array= np.zeros(N)
    comment= str()
    operation_num= 0
    comment += '\nBranch-And-Bound-----------------------------------------------------------------------------\n\n'

    def compute(node, x_iplusone, N, MAXWEIGHT, profit_list, weight_list):
        """
        Sub-algorithm comput for making child node.
        Input:
        node: the information of parent node.
        x_iplusone: 1 or 0. Whether this child node contains object x_i+1.
        N: the number of objects. It must be same with the length of profit_list and weight_list.
        MAXWEIGHT: the capacity of knapsack. It is given in input txt file.
        profit_list, weight_list: the lists of profit and weight of objects. It also is given by
                                input txt file, and opener() function make data into two lists.
        Output:
        the child node.

        *Note: the data structure of node is (ordering value, node), for using Priority Queue.
        Since the ordering value is Total profit of node, and since in python the priority is computed with
        ascending order, I take the ordering value of node to -Tprofit.
        """
        i= node['i']+ 1
        knapsack_array= copy.deepcopy(node['knapsack_array'])
        knapsack_array[i-1]= x_iplusone
        if x_iplusone:
            Tprofit= node['Tprofit']+ profit_list[i-1]
            Tweight= node['Tweight']+ weight_list[i-1]
            bound= Bd(i, Tprofit, Tweight, N, MAXWEIGHT, profit_list, weight_list)
        else:
            Tprofit= node['Tprofit']
            Tweight= node['Tweight']
            bound= Bd(i, Tprofit, Tweight, N, MAXWEIGHT, profit_list, weight_list)
        return (-Tprofit, {'node': (i, x_iplusone), 'i':i, 'knapsack_array': knapsack_array, 'Tprofit':Tprofit, 'Tweight':Tweight, 'bound':bound})

    # Initialize
    Priority_Q= queue.PriorityQueue()
    knapsack_array= np.zeros(N)
    i= 0
    Tprofit= 0
    Tweight= 0
    bound= Bd(i, Tprofit, Tweight, N, MAXWEIGHT, profit_list, weight_list)
    v_node= (-Tprofit, {'node': (i, 0), 'i':i, 'knapsack_array': knapsack_array, 'Tprofit':Tprofit, 'Tweight':Tweight, 'bound':bound})

    #put first node and run while loop
    Priority_Q.put(v_node)
    if add_comment: comment += 'Node inserted to PQ: '+ str(GetItemList(Priority_Q))+ '\n'
    while not Priority_Q.empty():
        node_todo= Priority_Q.get()[1]
        if add_comment:
            comment += 'Removed Node in PQ: '+ str(node_todo)+ \
                        '\n(The remaining PQ is: '+ str(GetItemList(Priority_Q))+ ')\n'
        operation_num += 1
        if node_todo['bound'] > max_profit: # Case when the bound of node is bigger than max_profit.
            # Left-side Node
            v_node= compute(node_todo, 1, N, MAXWEIGHT, profit_list, weight_list)
            if add_comment:
                comment += '\tCompute left-side node: '+ str(v_node[1])+ '\n'
            operation_num += 1
            if v_node[1]['bound']!= False and v_node[1]['Tprofit']> max_profit:
            #Case when Total profit of node is bigger than max_profit and the total weight of node does not exceeds MAXWEIGHT.
            # v_node[1]['bound']== False means the weight of this node is bigger than MAXWEIGHT.
                max_knapsack_array= copy.deepcopy(v_node[1]['knapsack_array'])
                max_profit= v_node[1]['Tprofit']
                if add_comment:
                    comment += '\t\tMaxProfit array changed: '+ str(max_knapsack_array)+\
                                '\tmax_profit: '+ str(max_profit)+ '\n'
            else:
            #Case when Total profit of node is not bigger than max_profit or the total weight of node does exceeds MAXWEIGHT.
                if add_comment: comment += '\t\tMaxProfit do not changed.\n'
            operation_num += 1
            if v_node[1]['bound'] > max_profit: # Decide whether or not the node must be inserted to Queue.
                Priority_Q.put(v_node)
                if add_comment:
                    comment += '\t\tNode inserted to PQ: '+ str(GetItemList(Priority_Q))+ '\n'
            else:
                if add_comment: comment += '\t\tNode not inserted to PQ: bound is too small.'+ '\n'
            # Right-side Node
            v_node= compute(node_todo, 0, N, MAXWEIGHT, profit_list, weight_list)
            if add_comment: comment += '\tCompute right-side node: '+ str(v_node[1])+ '\n'
            operation_num += 1
            if v_node[1]['bound'] > max_profit: # Decide whether or not the node must be inserted to Queue.
                Priority_Q.put(v_node)
                if add_comment: comment += '\t\tNode inserted to PQ: '+ str(GetItemList(Priority_Q))+ '\n'
            else:
                if add_comment: comment += '\t\tNode not inserted to PQ: bound is too small.'+ '\n'
        else:   # Case when the bound of node is not bigger than max_profit.
            if add_comment: comment += '\tDo not compute the child Node: bound is too small.\n'

    #the end of while loop.
    if add_comment:
        comment += 'Result array: '+ str(max_knapsack_array)+ '\tResult max_profit: '+ str(max_profit)+ '\n'
        comment+= '######## The number of operation is: '+ str(operation_num) + '\n'
    return (max_knapsack_array, max_profit)

# Analysis Function ############################################################
def all_possible_objects(N, PROFIT_SUM, WEIGHT_SUM):
    """
    as given a data of objects, we could compute the number of objects, sum of profits of all objects, and
    the sum of weights of all objects. I hypothesize the avg time-order and worst time-order as the average and maximum value of
    time-order with same number of objects, the capacity of knapsack, the sum of profits and sum of weights are all same.
    This function returns all possible lists of objects I could take in this hypothesis.

    *Note: It takes too much computing time...
            I've limited the length of possible case to 2,000,000, but if you want different value, you could change the value in function.
            If you just want naive result of algorithm, then turn off the 'analyze' when running the program.
    """
    global comment
    comment= str()
    PROFIT_SUM_by5= (PROFIT_SUM//5)
    Q= []
    possible_weight= []
    possible_profit= []
    possible_p_w= []
    weight_list= list(np.ones(N))
    profit_list= list(np.ones(N))
    # All possible lists of weights
    weight_list[0]= WEIGHT_SUM-N+1
    Q.append(weight_list)
    while not (Q== [] or Q[0][0] < 1):
        weight_list = Q.pop(0)
        weight_list= list(map(int, weight_list))
        if weight_list not in possible_weight: possible_weight.append(copy.deepcopy(weight_list))
        for j in range(N-1, 0, -1):
            weight_list2= copy.deepcopy(weight_list)
            weight_list2[0] -= 1
            weight_list2[j] += 1
            if weight_list2 not in Q: Q.append(weight_list2)
    # All possible lists of profits
    profit_list[0]= PROFIT_SUM_by5-N+1
    Q= list()
    Q.append(profit_list)
    while not (Q== [] or Q[0][0] < 1):
        profit_list = Q.pop(0)
        profit_list= list(map(int, profit_list))
        if profit_list not in possible_profit:
            possible_profit.append(list(map(lambda x: x*5, copy.deepcopy(profit_list))))
        for j in range(N-1, 0, -1):
            profit_list2= copy.deepcopy(profit_list)
            profit_list2[0] -= 1
            profit_list2[j] += 1
            if all(profit_list2[i] >= profit_list2[i+1] >0 for i in range(N-1)):
                if profit_list2 not in Q: Q.append(profit_list2)
    #Cartesian multiple of those two lists.
    for k1, w in enumerate(possible_weight):
        for k2, p in enumerate(possible_profit):
            (p_w_list, profit_list, weight_list)= list_sort(p, w)
            possible_p_w.append((profit_list, weight_list))
    if len(possible_p_w)> 2000000:
        random.shuffle(possible_p_w)
        possible_p_w= possible_p_w[:2000000]
    return possible_p_w

def statistic_run(func, N, MAXWEIGHT, PROFIT_SUM, WEIGHT_SUM, possible_p_w= None):
    """
    It iteratively runs the function to get the maximum value and average value of given function.
    When the algorithm is runned by this function, the commenting and writing in txt file is not taken.

    *Note: It also computes a lot. In my computer, the ovrall running time is almost 25 minutes.
    I recommend to do not turn on 'analyze' if you just want result.
    """
    global comment, operation_num
    comment= 0
    if not possible_p_w: possible_p_w= all_possible_objects(N, PROFIT_SUM, WEIGHT_SUM)
    op_list= []
    max_op= 0
    for elmt_list in possible_p_w:
        operation_num= 0
        func(N, MAXWEIGHT, elmt_list[0], elmt_list[1], add_comment= False)
        op_list.append(operation_num)
        if operation_num> max_op:
            max_op= operation_num
            max_op_list= elmt_list
    avg_op= sum(op_list)/len(possible_p_w)
    std_op= np.std(op_list)
    comment+= '\nThe hypothesis of"{}" algorithm is:\n'.format(func.__name__)
    comment+= '\tThe Algorithm that I\'ve run is: {};\t the Number of objects is: {}, Maximum of weights of knapsack is: {}, Sum of profits of objects is: {}, and Sum of weights of object is: {}\n'.format(func.__name__, N, MAXWEIGHT, PROFIT_SUM, WEIGHT_SUM)
    comment+= "I've produced all sets of objects which has same Number of objects, same Sum of weights, same Sum of profits of objects, but has different distributions and with different pairs.\n"
    comment+= 'And I build an algorithm for repeat 0/1 knapsack problem for every set of objects, and find out the average operation number and worst case operation number.\n'
    comment+= 'The number of sets of objects is {}:\n'.format(len(possible_p_w))
    comment+= '\tIn here, the Average operation number is {:.6f}, the Standard Deviation of operation is {:.6f}, the Worst-Case operation number is {} and one of the worst case profit & weight is {}.\n'.format(avg_op, std_op, max_op, max_op_list)
    return (avg_op, max_op, op_list)

# Run file #####################################################################

def write_all(inputfile= 'input.txt', outputfile= 'output.txt',list_func= [DP_K, BT_K, BB_K],\
                write_txt= True, add_comment= True, analyze= True):
    """
    when running the whole program, this program runs in the order of this function.
    It checks the input file, output file, the settings when running this value, and run the algorithms, and analyzing functions.
    """
    global comment, operation_num
    if len(sys.argv)>2:
        outputfile= sys.argv[2]
    if os.path.isfile(outputfile): os.remove(outputfile)
    (N, MAXWEIGHT, profit_list, weight_list)= opener(inputfile, ' ')

    for func in list_func:
        result_array, result_value= func(N, MAXWEIGHT, profit_list, weight_list,add_comment= add_comment)
        print(comment)
        if write_txt:
            writer(profit_list, weight_list, max_knapsack_array= result_array,\
                    comment=comment, max_profit= result_value, outputfile= outputfile)
    if analyze:
        possible_p_w= all_possible_objects(N, sum(profit_list), sum(weight_list))
        plt.figure(figsize=(11,4))
        for k, func in enumerate(list_func):
            (avg_op, max_op, op_list)= statistic_run(func, N, MAXWEIGHT,sum(profit_list), sum(weight_list), possible_p_w)
            print(comment)
            plt.subplot(1, len(list_func), k+1)
            plt.hist(op_list, bins= 50)
            plt.title(func.__name__)
            with open(outputfile, 'at') as f:
                if comment:
                    comment= comment+ '\n'
                    f.write(comment)
        plt.show()
    print('Algorithm ended; Check the result value, trace and analysis of algorithm in txt file.')

# __main__ #####################################################################
if __name__== '__main__':
    if len(sys.argv)>1:
        inputfile= sys.argv[1]
    else: inputfile= 'input.txt'
    if len(sys.argv)>2:
        outputfile= sys.argv[2]
    else: outputfile= 'output.txt'
    if len(sys.argv)<4:
        write_all(inputfile= inputfile, outputfile= outputfile, list_func= [DP_K, BT_K, BB_K],\
                        write_txt= True, add_comment= True, analyze= True)
    else:
        setting= sys.argv[3:]
        analyze, list_func, write_txt, add_comment= (True, [DP_K, BT_K, BB_K], True, True)
        for i in setting:
            i= i.split(':')
            print(i)
            if i[0]== "analyze":
                analyze= bool(int(i[1]))
            elif i[0]== "write_txt":
                write_txt= bool(int(i[1]))
            elif i[0]== "add_comment":
                add_comment= bool(int(i[1]))
        write_all(inputfile= inputfile, outputfile= outputfile, list_func= list_func,\
                        write_txt= write_txt, add_comment= add_comment, analyze= analyze)
