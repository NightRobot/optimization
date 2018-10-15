from openpyxl import load_workbook
from pprint import pprint
wb = load_workbook(filename='../../data/workload.xlsx')

servers = []
days = []
vm = []
for i in range(4):
	ws = wb['Sheet'+str(i+1)]
	for column in ws.columns:
	    for cell in column:
	        # print(cell.value)
	        vm.append(cell.value)

	    # print(vm)
	    days.append(vm)
	    vm = []
	# print(days)
	servers.append(days)
	days = []
print("result : ")
pprint(servers)
