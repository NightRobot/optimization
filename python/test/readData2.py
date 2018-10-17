from pprint import pprint
import pandas as pd

servers = []
days = []
vm = []
DAYS = [16,28,31]
for i in range(4):
	df = pd.read_excel('../../data/workload.xlsx',sheet_name='DC'+str(i+1), dtype={'name':str, 'id':str,'16':float,'28':float,'31':float})
	for j in range(len(DAYS)):
		for k in range( len ( df[DAYS[j]] )):
			print(df[DAYS[j]][k])

servers = []
days = []
vm = []
data = []
index = 0
for i in range(4):
	df = pd.read_excel('../../data/workload.xlsx',sheet_name='DC'+str(i+1), dtype={'name':str, 'id':str,'16':float,'28':float,'31':float})
	for j in range(len(DAYS)):
		for k in range( len ( df[DAYS[j]] )):
			print(df[DAYS[j]][k])
			# print(cell.value)
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
pprint(servers)