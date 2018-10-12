from openpyxl import load_workbook
wb = load_workbook(filename='Data.xlsx')

servers = []
days = []
vm = []
for i in range(SERVER):
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
print("result : ")
print(servers)

print(len(servers))
print(len(servers[0]))
print(len(servers[0][0]))

