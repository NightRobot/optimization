import random
import numpy as np
from itertools import combinations
from openpyxl import load_workbook,Workbook
from pprint import pprint

SERVERS = 4
DAYS = 3
NUMBER_OF_ITERATION = 0

def find_sum_workload(workload) :
    tmp = 0
    a = [[0 for j in range(len(workload[i]))] for i in range(len(workload))] 
    # print(a)
    for i in range(len(workload)) :
        for j in range(len(workload[i])) :
    #         tmp = np.amax(workload[i][j])
            for k in range(len(workload[i][j])) :

                tmp = tmp + workload[i][j][k]

            # print(tmp)
            # print(i,j)
            a[i][j] = tmp
            tmp = 0
    return a
def find_max_of_each_server(a):
    B = [0 for i in range(len(a))]
    for i in range(len(a)) :
        B[i] = max(a[i])
    return B

def find_avg_of_wvm_per_server(workload) :
    
    avg_vm = 0
    tmp = 0
    avg_WVM = [[0 for k in range(len(workload[i][0]))] for i in range(len(workload))]
    for i in range(len(workload)) :
        for k in range(len(workload[i][0])) :
            tmp = tmp + workload[i][0][k] + workload[i][1][k] + workload[i][2][k] 
        #     print(tmp)
            avg_vm = tmp/3
            avg_WVM[i][k] = avg_vm
            tmp = 0
    return avg_WVM
    
def iteration_calculate(workload):
	# # create tmp variable
	a_tmp = find_sum_workload(workload)
	B_tmp = find_max_of_each_server(a_tmp)

	# print("avg")
	avg_WVM_tmp = find_avg_of_wvm_per_server(workload)
	# print(avg_WVM_tmp)
	
	# print("sort")
	sort_avg_WVM = sort_wvm(avg_WVM_tmp)
	# print(sort_avg_WVM)

	### fix bug sort
	avg_WVM_tmp = find_avg_of_wvm_per_server(workload)

	P = max(B_tmp)
	index_serverP = B_tmp.index(P)
	Q = min(B_tmp)
	index_serverQ = B_tmp.index(Q)
	# list_workload_tmp = np.array(workload_tmp).tolist()

	MAX_WORKLOAD_OF_SERVER_CURRENT = P
	# print("current MAX : ",MAX_WORKLOAD_OF_SERVER_CURRENT)
	MAX_WORKLOAD_OF_SERVER_NEW = 0

	VM_in_serverP = len(workload[index_serverP][0])
	save = []
	# print("move ",index_serverP,"to ",index_serverQ)
	for q in range(1):
	    # print("select vms ",q+1)
	    # Combination algorithms
	    # list of Combination data use to select vm in server p
	    combination = list(combinations(range(VM_in_serverP),q+1))
	    select_num = 0
	    # print("start iteration")
	    while MAX_WORKLOAD_OF_SERVER_CURRENT > MAX_WORKLOAD_OF_SERVER_NEW :
	#         print('Combination ',combination[pointer])
	#         print('range ',len(combination[pointer]))
	        a_tmp = find_sum_workload(workload)
	        if MAX_WORKLOAD_OF_SERVER_NEW != 0 :
	            MAX_WORKLOAD_OF_SERVER_CURRENT = MAX_WORKLOAD_OF_SERVER_NEW
	        # print("current workload compare ",MAX_WORKLOAD_OF_SERVER_CURRENT)
	        # combination loop to test selection
	        vm_list = []
	#         print(combination[select_num])
	        # print("old a")    
	        # print(a_tmp)
	        for l in range(len(combination[select_num])) : 
	            k = combination[select_num][l]
	            select_value = sort_avg_WVM[index_serverP][k]
	            # print(select_value)
	            index_vm = avg_WVM_tmp[index_serverP].index(select_value)
	#             print(index_vm)  
	            vm_list.append(index_vm)
	            
	#             tmp_workload = tmp_workload + select_value
	            
	            for j in range(len(workload[index_serverP])) :
	                # print("move workload vm ",index_vm,workload[index_serverP][j][index_vm])
	                
	                a_tmp[index_serverQ][j] = a_tmp[index_serverQ][j] + workload[index_serverP][j][index_vm]
	                a_tmp[index_serverP][j] = a_tmp[index_serverP][j] - workload[index_serverP][j][index_vm]
	        # print("new a")
	        # print(a_tmp)

	        B_tmp = find_max_of_each_server(a_tmp)
	        MAX_WORKLOAD_OF_SERVER_NEW = max(B_tmp)
	        
	        if MAX_WORKLOAD_OF_SERVER_CURRENT > MAX_WORKLOAD_OF_SERVER_NEW :
	            save.insert(q,[vm_list,MAX_WORKLOAD_OF_SERVER_NEW])
	            
	        select_num = select_num + 1
	    
	    a_tmp = find_sum_workload(workload)
	    B_tmp = find_max_of_each_server(a_tmp)
	    MAX_WORKLOAD_OF_SERVER_CURRENT = P   
	    MAX_WORKLOAD_OF_SERVER_NEW = 0
	    
	#         MAX_WORKLOAD_OF_SERVER_NEW = 1000
	#     break
	a = find_sum_workload(workload)
	B = find_max_of_each_server(a)
	return save

def sort_wvm(data):
	for i in range(len(data)):
		# print(data[i])
		data[i].sort()
	# print(sort_avg_WVM)		
	return data

def readData(file) :
	wb = load_workbook(filename=file)
	servers = []
	days = []
	vm = []
	for i in range(4):
		ws = wb['Sheet'+str(i+1)]
		for column in ws.columns:
		    for cell in column:
		        # print(cell.value)
		        vm.append(float(cell.value))

		    # print(vm)
		    days.append(vm)
		    vm = []
		# print(days)
		servers.append(days)
		days = []
	# pprint(servers)
	return servers
	
if __name__ == "__main__":
	workload = readData("data/Data.xlsx")
	# print(workload)

	# keyboard input number of iteration
	NUMBER_OF_ITERATION = int(input("Number of Iteration : "))
	for i in range(NUMBER_OF_ITERATION) :
		a = find_sum_workload(workload)
		B = find_max_of_each_server(a)
		# print("before move")
		# pprint(a)
		# pprint(B)

		"""
		print("avg")
		avg_WVM = find_avg_of_wvm_per_server(workload)
		print(avg_WVM)
		
		print("sort")
		sort_avg_WVM = sort_wvm(avg_WVM)
		print(sort_avg_WVM)
		"""

		# Maximum workload P
		P = max(B)
		index_serverP = B.index(P)
		# print(P)
		# print(index_serverP)
		# Minimum wokload Q
		
		Q = min(B)
		index_serverQ = B.index(Q)
		# print(Q)
		# print(index_serverQ)
		print("move from ",index_serverP,"to ",index_serverQ)
		print("running iteration "+str(i)+ "!!!")

		save = iteration_calculate(workload)

		# print("iteration done!!!")

		print("select vm to best move in iteration")
		# pprint(save)
		if len(save) == 0 :
			print("can't move vm for best max")
			break

		select = save[0]
		compare = []
		for i in range(len(save)):
			compare = save[i]
		#     print(select[1],"vs",compare[1])
			if select[1] > compare[1] :
				select = compare

		print(select)

		select_vm = select[0]
		# print("select vm ",select_vm)

		# print("move vm instruction")
		

		### move vm from serverP to serverQ
		vm_to_move = []
		wvm = 0
		vm_move_in_serverP_per_days = []
		for j in range(len(workload[index_serverP])) :
			# print("j",j)
			for k in range(len(select_vm)) :
				# print("k",k)
				# print(select_vm[k])
				wvm = workload[index_serverP][j][select_vm[k]]
				# print(wvm)
				vm_to_move.append([ select_vm[k] ,workload[index_serverP][j][select_vm[k]] ])

				# move

				workload[index_serverQ][j].append(wvm)
				wvm = 0
			vm_move_in_serverP_per_days.append(vm_to_move)
			vm_to_move = []

		# pprint(vm_move_in_serverP_per_days)
		### remove vm from serverP
		for j in range(len(vm_move_in_serverP_per_days)) :
			# print(vm_move_in_serverP_per_days[j])
			for k in range(len(vm_move_in_serverP_per_days[j])):
				# print(vm_move_in_serverP_per_days[j][k])
				# remove
				workload[index_serverP][j].remove(vm_move_in_serverP_per_days[j][k][1])


		# print("new workload")		
		# pprint(workload)


		a = find_sum_workload(workload)
		print("after move ")
		# a = workload.sum(axis=2)
		pprint(a) # calculate aij
		B = find_max_of_each_server(a)
		# B = np.amax(a,axis=1)
		pprint(B) # bij
		# pprint(vm_move_in_serverP_per_days)
