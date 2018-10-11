
# VM Relocate Optimixation Integer programming

import pulp
import pandas as pd
from openpyxl import load_workbook
from pprint import pprint
SERVERS = 4
DAYS = 3
VM = 58
WORKLOAD = []
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
    WORKLOAD = pd.DataFrame.from_csv('Data/workload_per_days.csv',index_col = ['vm','day'])
    pprint(WORKLOAD);
    W = pulp.LpVariable.dicts("W",
                                     ((vm, day) for vm, day in WORKLOAD.index),
                                     lowBound=0,
                                     cat='Continuous')
    pprint(W)
    X = pulp.LpVariable.dicts("X",
                                     ((vm, server) for vm in range(VM) for server in range(SERVERS)),
                                     cat='Binary')
    pprint(X)
    