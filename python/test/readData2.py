from pprint import pprint
import pandas as pd

servers = []
days = []
vm = []
for i in range(4):
	df = pd.read_excel('../../data/workload.xlsx',sheet_name='DC'+str(i+1), dtype={'name':str, 'id':str,'16':float,'28':float,'31':float})
	servers.append(df)
print("result : ")
print(servers)

# pprint(servers)