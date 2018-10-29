import random,time,csv
import numpy as np
import pandas as pd
from itertools import combinations
from pprint import pprint

SERVERS = 0
KEYS = []
NUMBER_OF_ITERATION = 0
NUMBER_VM_TO_MOVE = 0
LIST_NAME_VM = []
RELOCATE_VM = []
REDUNDANCES = []
GROUPS = []
LOCKS = []
# * declare for variable use in code
# i is server
# j is day
# k is vm
# workload data format
# [   server 1
#     [  
#         [ 'vm' , [wvm1],[wvm2],[wvm3] ],
#         [ 'vm' , [wvm1],[wvm2],[wvm3] ],
#         ...
#         [ 'vm' , [wvm1],[wvm2],[wvm3] ]
#     ],
#     server 2
#     [
#         [ 'vm' , [wvm1],[wvm2],[wvm3] ],
#         [ 'vm' , [wvm1],[wvm2],[wvm3] ],
#         ...
#         [ 'vm' , [wvm1],[wvm2],[wvm3] ]
#     ],
#     ...
# ]

# * function workload
def find_sum_workloads(workloads) :
    sum_workload = []
    data = []
    tmp = 0
    for server in workloads :
        # print(server)
        for day in range(len(KEYS[2:])):
            for vm in server : 
                # print(day)
                # print(vm)
                # print(vm[1][day])
                tmp += vm[1][day]
            # print(tmp)
            data.append(tmp)
            tmp = 0
        sum_workload.append(data)
        data = []
    # print(sum_workload)  
    return sum_workload

def find_max_of_each_server(sum_workload) :
    max_workload = []
    for server in sum_workload :
        # print(server)
        # print(max(server))
        max_workload.append(max(server))
    # print(max_workload)
    return max_workload

def find_avg_of_wvm_per_server(workloads) :
    avg_workload = []
    data = []
    tmp = 0
    for server in workloads :
        for vm in server :
            for day in range(len(vm[1])):
                tmp += vm[1][day]
            tmp = tmp/len(vm[1])
            # print(tmp)
            data.append([vm[0],tmp])
            tmp = 0
        # pprint(servers)
        avg_workload.append(data)
        data = []
    # pprint(avg_workload)
    return avg_workload

# * function iteration caluclate
def iteration_calculate(workloads):
    # # create tmp variable
    a_tmp = find_sum_workloads(workloads)
    B_tmp = find_max_of_each_server(a_tmp)

    ### fix bug sort
    avg_WVM_tmp = find_avg_of_wvm_per_server(workloads)

    P = max(B_tmp)
    index_serverP = B_tmp.index(P)
    Q = min(B_tmp)
    index_serverQ = B_tmp.index(Q)

    MAX_WORKLOAD_OF_SERVER_CURRENT = P
    # print("current MAX : ",MAX_WORKLOAD_OF_SERVER_CURRENT)
    MAX_WORKLOAD_OF_SERVER_NEW = 0

    VM_in_serverP = len(workloads[index_serverP])
    save = []
    # print("move ",index_serverP,"to ",index_serverQ)
    for q in range(NUMBER_VM_TO_MOVE):
        # print("select vms ",q+1)
        # Combination algorithms
        # list of Combination data use to select vm in server p
        combination = list(combinations(range(VM_in_serverP),q+1))
        combi_num = 0
        # print(combination)
        # print("number of combination is ",len(combination))
        # print("start iteration")
        
        # start iteration
        for num in range(len(combination)) :
        # while MAX_WORKLOAD_OF_SERVER_CURRENT > MAX_WORKLOAD_OF_SERVER_NEW :
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
                
                vm_list.append([ k,workloads[index_serverP][k][0] ])
                for j in range(len(KEYS[2:])) :
                    # print("move workload vm ",index_vm,workloads[index_serverP][j][index_vm][0])
                    # 1 is data in workload format
                    # [ 'vm' , [wvm],[wvm],[wvm]]
                    a_tmp[index_serverQ][j] = a_tmp[index_serverQ][j] + workloads[index_serverP][k][1][j]
                    a_tmp[index_serverP][j] = a_tmp[index_serverP][j] - workloads[index_serverP][k][1][j]
            # print("new a")
            # print(a_tmp)
            B_tmp = find_max_of_each_server(a_tmp)
            MAX_WORKLOAD_OF_SERVER_NEW = max(B_tmp)
            # print("current MAX NEW : ",MAX_WORKLOAD_OF_SERVER_NEW)
            # * save format [ [vm list] ,Maximum workload ]
            save.insert(q,[vm_list,MAX_WORKLOAD_OF_SERVER_NEW])

            
            # if MAX_WORKLOAD_OF_SERVER_CURRENT > MAX_WORKLOAD_OF_SERVER_NEW :
                
                # save.insert(q,[vm_list,MAX_WORKLOAD_OF_SERVER_NEW])

            combi_num = combi_num + 1
        
        a_tmp = find_sum_workloads(workloads)
        B_tmp = find_max_of_each_server(a_tmp)
        MAX_WORKLOAD_OF_SERVER_CURRENT = P   
        MAX_WORKLOAD_OF_SERVER_NEW = 0
        
            # MAX_WORKLOAD_OF_SERVER_NEW = 
        # 1000
        # break
    a = find_sum_workloads(workloads)
    B = find_max_of_each_server(a)
    return save

# TODO function redundacy
def redundnacy_move (workloads):
    # pprint(REDUNDANCES)
    save = []
    for redun in REDUNDANCES :
        print(redun)
    return save

# TODO function grouping
def group_move (workloads):
    # pprint(GROUPS)
    save = []

    return save

# TODO checking locking list
def lock_checking (select):
    # pprint(LOCKS)
    found = False
    lock_list = LOCKS[0]
    vm_list = select[0]
    # print(select)
    # print(lock_list)
    # print(vm_list)
    for lock in lock_list :
        for vm in vm_list :
            # print(lock)
            # print(vm[1])
            if lock == vm[1] :
                # print("found")
                found = True
    return found

# * function read csv data redundancy list workload
def readCSV (filelocate) :
    groups = []
    with open(filelocate, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            groups.append(row)
        # print(groups)
    return groups

# * function read data from file then convert to worklaod data format
def readExcel(file):
    xlsx = pd.ExcelFile(file)
    workload_sheet = []
    for sheet in xlsx.sheet_names:
        workload_sheet.append(xlsx.parse(sheet))
    return workload_sheet

# * function convert data from sheet to workload format 
def getData(workload_sheet) :
    workload = []
    servers = []
    data = []
    vm = []
    for server in workload_sheet : 
        index = server.index.tolist()
        # print(index)
        # print(server)
        for k in index :    
            # print("vm : ",k)
            # print(KEYS)
            for j in KEYS[2:] :
                # print(j)
                # print(server[j][k])
                data.append(server[j][k])
            # print("data : ",data)
            vm.append(server["name"][k])
            vm.append(data)
            # pprint(vm)
            servers.append(vm)
            data = []
            vm = []
        # pprint(servers)
        workload.append(servers)
        servers = []
    # pprint(workload)
    return workload

# * main program
if __name__ == "__main__":
    workload_sheet = readExcel("../data/workload_aug2018.xlsx")
    REDUNDANCES = readCSV("../data/redundancylist.csv")
    GROUPS = readCSV("../data/grouplist.csv")
    LOCKS  = readCSV("../data/locklist.csv")
    # print(workload_sheet)
    # * setup the constant var
    KEYS = workload_sheet[0].keys().values.tolist()
    # print(KEYS)
    SERVERS = len(workload_sheet)
    # print(SERVERS)
    
    workloads = getData(workload_sheet)
    # pprint(workload)

    sum_workload = find_sum_workloads(workloads)
    max_workload = find_max_of_each_server(sum_workload)
    avg_workload = find_avg_of_wvm_per_server(workloads)
    print("Maximum Workload")
    print(sum_workload)
    print(max_workload)
    # pprint(avg_workload)

    print("-------------------------------------------------------------------------")

    # * keyboard input number of iteration
    NUMBER_OF_ITERATION = int(input("Number of Iteration : "))
    NUMBER_VM_TO_MOVE = int(input("Number of VM to move : "))

    print("-------------------------------------------------------------------------")
    start = time.time()
    for i in range(NUMBER_OF_ITERATION) :
        a = find_sum_workloads(workloads)
        B = find_max_of_each_server(a)
        print("before move")
        pprint(a)
        pprint(B)

        # Maximum workloads P
        P = max(B)
        index_serverP = B.index(P)
        print("MAX in server ",P)
        print(index_serverP)

        # Minimum wokload Q
        Q = min(B)
        index_serverQ = B.index(Q)
        print("MIN in server ",Q)
        print(index_serverQ)

        print("running iteration "+str(i+1)+ "!!!")
        print("move from ",index_serverP,"to ",index_serverQ)
        
        save = iteration_calculate(workloads)

        # print("iteration done!!!")
        # print("select vm to best move in iteration")
        # pprint(save)

        # * compare data in save iteration optimaization algorithms
        select = save[0]
        compare = []

        for n in range(len(save)):
            compare = save[n]
            # print(select[1],"vs",compare[1])
            # * compare maximum workload ,index 1 is 'Maximum workload after move'
            found = lock_checking(compare)
            if found == False :
                if select[1] > compare[1] :
                    select = compare

        # print(select)
        # check name of vm that selected
        num = 0
        select_vm = select[0]

        # print("select vm ",select_vm)
        # print("max workload in iteration ",select[1])

        # * condition to stop continue iteration
        if select[1] > max(B) :
            print("can't move vm for best max")
            print("-------------------------------------------------------------------------")
            break

        # print("move vm instruction")
        # RELOCATE_VM.append(select_vm)

        # * move vm from serverP to serverQ
        vm_to_move = []
        wvm = 0
        vm_move_in_serverP_per_days = []
        
        # * move vm in server P to server Q
        for k in range(len(select_vm)) :
            # print("k",k)
            # print(select_vm[k])

            # index 0 is 'index of vm in server P' need to move out
            wvm = workloads[index_serverP][select_vm[k][0]]
            # print(wvm)

            vm_to_move.append(wvm)
            workloads[index_serverQ].append(wvm)
            
            wvm = 0
        # pprint(vm_to_move)
        # * remove vm from serverP
        for wvm in vm_to_move:
            # remove
            # * index 0 is 'index of vm in server P' need to move out
            # print("remove ",wvm)
            workloads[index_serverP].remove(wvm)
        
        # * list vm that move in iteration 
        list_of_vm = []
        for k in range(len(select_vm)) :
            # index 1 is 'name of vm in server P' to move out
            list_of_vm.append( select_vm[k][1] )
        RELOCATE_VM.append([list_of_vm,str(index_serverP)+" move to "+str(index_serverQ)])
        list_of_vm = []

        ## show result in iteration 
        a = find_sum_workloads(workloads)
        # print("after move ")
        pprint(a) # calculate aij
        B = find_max_of_each_server(a)
        pprint(B) # bij
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
    # for i in range(SERVERS):
    #     print("server ",i)
    #     pprint(workloads[i][0])
    print("-------------------------------------------------------------------------")
    end = time.time()
    print("Executed time ",end - start)
    print("-------------------------------------------------------------------------")