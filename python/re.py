import random,time,csv
import numpy as np
import pandas as pd
from itertools import combinations
from pprint import pprint

SERVERS = 4
DAYS = [16,28,31]
NUMBER_OF_ITERATION = 0
NUMBER_VM_TO_MOVE = 2
OVSAPP = [[3.944,3.989,4.129]
         ,[3.911,3.823,3.808]
         ,[1.606,1.74,1.149]
         ,[2.208,2.678,2.678]]
LIST_NAME_VM = []
RELOCATE_VM = []
REDUNDANCE = []
""
def find_sum_workloads(workloads) :
    tmp = 0
    a = [[0 for j in range(len(workloads[i]))] for i in range(len(workloads))] 
    # print(a)
    for i in range(len(workloads)) :
        for j in range(len(workloads[i])) :
            # tmp = np.amax(workloads[i][j])
            for k in range(len(workloads[i][j])) :

                tmp = tmp + workloads[i][j][k][0]

            # print(tmp)
            # print(i,j)
            a[i][j] = tmp + OVSAPP[i][j]
            tmp = 0
    return a
def find_max_of_each_server(a):
    B = [0 for i in range(len(a))]
    for i in range(len(a)) :
        B[i] = max(a[i])
    return B

def find_avg_of_wvm_per_server(workloads) :
    
    avg_vm = 0
    tmp = 0
    avg_WVM = [[0 for k in range(len(workloads[i][0]))] for i in range(len(workloads))]
    for i in range(len(workloads)) :
        for k in range(len(workloads[i][0])) :
            tmp = tmp + workloads[i][0][k][0] + workloads[i][1][k][0] + workloads[i][2][k][0]
            # print(tmp)
            avg_vm = tmp/3
            avg_WVM[i][k] = avg_vm
            tmp = 0
    return avg_WVM

def readCSV (filelocate) :
    groups = []
    with open(filelocate, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            groups.append(row)
        # print(groups)
    return groups

def readData(file) :
    servers = []
    days = []
    vm = []
    data = []
    index = 0
    for i in range(SERVERS):
        df = pd.read_excel(file,sheet_name='DC'+str(i+1)    )
        for j in range(len(DAYS)):
            for k in range( len ( df[DAYS[j]] )):
                print(df[DAYS[j]][k])
                data.append(float(df[DAYS[j]][k]))
                data.append(df["name"][k])
                vm.append(data)
                data = []
                index += 1
            index = 0
            # print(vm)
            days.append(vm)
            vm = []
        # print(days)
        servers.append(days)
        days = []
    # pprint(servers)
    return servers
def iteration_calculate(workloads):
    # # create tmp variable
    a_tmp = find_sum_workloads(workloads)
    B_tmp = find_max_of_each_server(a_tmp)

    # print("avg")
    # avg_WVM_tmp = find_avg_of_wvm_per_server(workloads)
    # print(avg_WVM_tmp)
    
    # print("sort")
    # sort_avg_WVM = sort_wvm(avg_WVM_tmp)
    # print(sort_avg_WVM)

    ### fix bug sort
    avg_WVM_tmp = find_avg_of_wvm_per_server(workloads)

    P = max(B_tmp)
    index_serverP = B_tmp.index(P)
    Q = min(B_tmp)
    index_serverQ = B_tmp.index(Q)

    MAX_WORKLOAD_OF_SERVER_CURRENT = P
    # print("current MAX : ",MAX_WORKLOAD_OF_SERVER_CURRENT)
    MAX_WORKLOAD_OF_SERVER_NEW = 0

    VM_in_serverP = len(workloads[index_serverP][0])
    save = []
    # print("move ",index_serverP,"to ",index_serverQ)
    for q in range(NUMBER_VM_TO_MOVE):
        # print("select vms ",q+1)
        # Combination algorithms
        # list of Combination data use to select vm in server p
        combination = list(combinations(range(VM_in_serverP),q+1))
        combi_num = 0
        # print("number of combination is ",len(combination))
        # print("start iteration")
        
        # start iteration
        for num in range(len(combination)) :
        # while MAX_WORKLOAD_OF_SERVER_CURRENT > MAX_WORKLOAD_OF_SERVER_NEW :
            # print('Combination ',combination[pointer])
            # print('range ',len(combination[pointer]))
            a_tmp = find_sum_workloads(workloads)
            if MAX_WORKLOAD_OF_SERVER_NEW != 0 :
                MAX_WORKLOAD_OF_SERVER_CURRENT = MAX_WORKLOAD_OF_SERVER_NEW
            # print("current workload compare ",MAX_WORKLOAD_OF_SERVER_CURRENT)
            
            # combination loop to test selection
            vm_list = []
            # print(combination[combi_num]) 
            # print("old a")    
            # print(a_tmp)
            for l in range(len(combination[combi_num])) : 
                k = combination[combi_num][l]
                
                vm_list.append([k,workloads[index_serverP][0][k][1]])
                for j in range(len(workloads[index_serverP])) :
                    # print("move workload vm ",index_vm,workloads[index_serverP][j][index_vm][0])
                    
                    a_tmp[index_serverQ][j] = a_tmp[index_serverQ][j] + workloads[index_serverP][j][k][0]
                    a_tmp[index_serverP][j] = a_tmp[index_serverP][j] - workloads[index_serverP][j][k][0]
            # print("new a")
            # print(a_tmp)
            B_tmp = find_max_of_each_server(a_tmp)
            MAX_WORKLOAD_OF_SERVER_NEW = max(B_tmp)
            # print("current MAX NEW : ",MAX_WORKLOAD_OF_SERVER_NEW)
            save.insert(q,[vm_list,MAX_WORKLOAD_OF_SERVER_NEW])

            
            # if MAX_WORKLOAD_OF_SERVER_CURRENT > MAX_WORKLOAD_OF_SERVER_NEW :
                
            #     save.insert(q,[vm_list,MAX_WORKLOAD_OF_SERVER_NEW])

            combi_num = combi_num + 1
        
        a_tmp = find_sum_workloads(workloads)
        B_tmp = find_max_of_each_server(a_tmp)
        MAX_WORKLOAD_OF_SERVER_CURRENT = P   
        MAX_WORKLOAD_OF_SERVER_NEW = 0
        
        #     MAX_WORKLOAD_OF_SERVER_NEW = 1000
        # break
    a = find_sum_workloads(workloads)
    B = find_max_of_each_server(a)
    return save

# check redundance for vm that need to move
def redun(workloads,index_serverP,index_serverQ,list_vm_to_move):
    redun = False
    con = 0
    # pprint(REDUNDANCE)
    # print(workloads[index_serverP][0])
    # print("list vm to move")
    # print(list_vm_to_move)

    for vm in list_vm_to_move :
        name = vm[1]
        con = 0
        # print(name)
        for i in range(len(REDUNDANCE)) :
            # print(REDUNDANCE[i])
            # Check redundance list
            found = name in REDUNDANCE[i]
            if found == True :
                # print("in redundance list ")
                # print(i)
                for vm in workloads[index_serverQ][0]:
                    # print(vm[1])
                    found = vm[1] in REDUNDANCE[i]
                    if found == True :
                        con += 1
                        break
                if con >= 1 :
                    # print("dont move ")
                    redun = False
                    break
                else :
                    # print("can move ")
                    redun = True
                con = 0
            else :
                # print("not in redundance list ")
                redun = True
        if con >= 1 :
            break
    return redun


if __name__ == "__main__":
    workloads = readData("../data/workloadredun_update_241018.xlsx")
    
    REDUNDANCE = readCSV("../data/redundancylist.csv")
    # pprint(REDUNDANCE)
    # keyboard input number of iteration
    NUMBER_OF_ITERATION = int(input("Number of Iteration : "))
    NUMBER_VM_TO_MOVE = int(input("Number of VM to move : "))
    print("-------------------------------------------------------------------------")
    # pprint(workloads) 
    
    start = time.time()
    
    for i in range(NUMBER_OF_ITERATION) :
        a = find_sum_workloads(workloads)
        B = find_max_of_each_server(a)

        """
        print("avg")
        avg_WVM = find_avg_of_wvm_per_server(workloads)
        print(avg_WVM)
        
        print("sort")
        sort_avg_WVM = sort_wvm(avg_WVM)
        print(sort_avg_WVM)
        """

        # Maximum workloads P
        P = max(B)
        index_serverP = B.index(P)
        # print(P)
        # print(index_serverP)
        # Minimum wokload Q
        
        Q = min(B)
        index_serverQ = B.index(Q)
        # print(Q)
        # print(index_serverQ)
        print("running iteration "+str(i+1)+ "!!!")
        print("move from ",index_serverP,"to ",index_serverQ)
        print("before move")
        pprint(a)
        pprint(B)

        save = iteration_calculate(workloads)

        # print("iteration done!!!")

        # print("select vm to best move in iteration")
        # pprint(save)
        # condition to stop continue iteration

        select = save[0]
        compare = []
        n = 0
        while redun(workloads,index_serverP,index_serverQ,select[0]) == False :
            # print("select element can't move")
            save.pop(0)
            # print("remove ",save.pop(0))
            select = save[0]
            n += 1
            # print("current select : ",select)
            
        for n in range(len(save)):
            compare = save[n]
            # print(select,"vs",compare)
            if select[1] > compare[1] :
                select = compare
                # print("check redun")
                if redun(workloads,index_serverP,index_serverQ,compare[0]) == True :
                    # print("can move")
                    select = compare
                    # print(select)
                else :
                    # print("dont move")
                    # print(compare)
                    # print("")
        
        # print(select)
        # check name of vm that selected
        num = 0
        select_vm = select[0]
        print("select vm ",select_vm)
        # print("max workload in iteration ",select[1])
        if select[1] > max(B) :
            print("can't move vm for best max")
            print("-------------------------------------------------------------------------")
            break
        # print("move vm instruction")
        # RELOCATE_VM.append(select_vm)

        ### move vm from serverP to serverQ
        vm_to_move = []
        wvm = 0
        vm_move_in_serverP_per_days = []
        # print("number of vm in server P ",len(workloads[index_serverP][j]))
        for j in range(len(workloads[index_serverP])) :
            # print("j",j)
            for k in range(len(select_vm)) :
                # print("k",k)
                # print(select_vm[k])
                wvm = workloads[index_serverP][j][select_vm[k][0]]
                # print(wvm)
                vm_to_move.append([ select_vm[k][0] ,wvm ])
                workloads[index_serverQ][j].append(wvm)
                
                wvm = 0
            vm_move_in_serverP_per_days.append(vm_to_move)
            vm_to_move = []

        # pprint(vm_move_in_serverP_per_days)
        ### remove vm from serverP
        for j in range(len(vm_move_in_serverP_per_days)) :
            # print(vm_move_in_serverP_per_days[j])
            for k in range(len(vm_move_in_serverP_per_days[j])):
                # print(vm_move_in_serverP_per_days[j][k][1])
                # remove
                workloads[index_serverP][j].remove(vm_move_in_serverP_per_days[j][k][1])
        
        list_of_vm = []
        for k in range(len(select_vm)) :
                list_of_vm.append([ select_vm[k][1] ])
        RELOCATE_VM.append([list_of_vm,str(index_serverP+1)+" move to "+str(index_serverQ+1)])
        list_of_vm = []
        a = find_sum_workloads(workloads)
        print("after move ")
        pprint(a) # calculate aij
        B = find_max_of_each_server(a)
        pprint(B) # bij
        print(max(B))
        print("-------------------------------------------------------------------------")
                

        # print("new workloads")        
        # pprint(workloads)

    
    print("result : ")
    a = find_sum_workloads(workloads)
    # pprint(a) # calculate aij
    B = find_max_of_each_server(a)
    pprint(B) # bij
    print(max(B))
    print("-------------------------------------------------------------------------")
    print("Number of Iteration is ",len(RELOCATE_VM))
    print("vm to Relocate ")
    pprint(RELOCATE_VM)
    print("-------------------------------------------------------------------------")
    # for i in range(SERVERS):
    #     print("server ",i)
    #     pprint(workloads[i][0])
    
    end = time.time()
    print("Executed time ",end - start)
    print("-------------------------------------------------------------------------")
    
