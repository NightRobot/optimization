import random,time,csv
import numpy as np
import pandas as pd
from itertools import combinations
from pprint import pprint

SERVERS = 0
KEYS = []
NUMBER_OF_ITERATION = 0
NUMBER_VM_TO_MOVE = 0


def find_sum_workloads(workloads) :
    sum_workload = []
    data = []
    tmp = 0
    for server in workloads :
    #     print(server)
        for day in range(len(KEYS[2:])):
            for vm in server : 
    #             print(day)
    #             print(vm)
    #             print(vm[1][day])
                tmp += vm[1][day]
    #         print(tmp)
            data.append(tmp)
            tmp = 0
        sum_workload.append(data)
        data = []
    # print(sum_workload)  
    return sum_workload
def find_max_of_each_server(sum_workload) :
    max_workload = []
    for server in sum_workload :
    #     print(server)
    #     print(max(server))
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
    #         print(tmp)
            data.append([vm[0],tmp])
            tmp = 0
    #     pprint(servers)
        avg_workload.append(data)
        data = []
    # pprint(avg_workload)
    return avg_workload
def readCSV (filelocate) :
    groups = []
    with open(filelocate, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            groups.append(row)
        # print(groups)
    return groups

def readExcel(file):
    xlsx = pd.ExcelFile(file)
    workload_sheet = []
    for sheet in xlsx.sheet_names:
        workload_sheet.append(xlsx.parse(sheet))
    return workload_sheet
def getData(workload_sheet) :
    workload = []
    servers = []
    data = []
    vm = []
    for server in workload_sheet : 
        index = server.index.tolist()
        print(index)
        print(server)
        for k in index :    
            print("vm : ",k)
            print(KEYS)
            for j in KEYS[2:] :
                print(j)
                print(server[j][k])
                data.append(server[j][k])
            print("data : ",data)
            vm.append(server["name"][k])
            vm.append(data)
            pprint(vm)
            servers.append(vm)
            data = []
            vm = []
        pprint(servers)
        workload.append(servers)
        servers = []
    pprint(workload)
    return workload

if __name__ == "__main__":
    workload_sheet = readExcel("../data/workload_aug2018.xlsx")
    # print(workload_sheet)

    # setup the constant var
    KEYS = workload_sheet[0].keys().values.tolist()
    print(KEYS)
    SERVERS = len(workload_sheet)
    print(SERVERS)
    
    workloads = getData(workload_sheet)
    # pprint(workload)

    # keyboard input number of iteration
    # NUMBER_OF_ITERATION = int(input("Number of Iteration : "))
    # NUMBER_VM_TO_MOVE = int(input("Number of VM to move : "))

    print("-------------------------------------------------------------------------")
    sum_workload = find_sum_workloads(workloads)
    max_workload = find_max_of_each_server(sum_workload)
    avg_workload = find_avg_of_wvm_per_server(workloads)
    print(sum_workload)
    print(max_workload)
    pprint(avg_workload)