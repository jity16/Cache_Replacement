import os
path = os.getcwd()
filenames = os.listdir(path)
file = []
Instructions = []
CPI =[]
MissRate =[]

for filename in filenames:
	if filename.find('stats') != -1:
		print("file name :" + filename);
		name = filename.split('.')
		file.append(name[1])
		with open(filename,'r') as x:
			lines = x.readlines()
			for line in lines:
				if 'CPI' in line:
					line_array = line.strip('\n').split(" ")
					print(line_array[3] + ":" +line_array[4])	#Instructions
					Instructions.append(line_array[4])
					print(line_array[7] + ":" +line_array[8])	#CPI
					CPI.append(line_array[8])
					break
			miss = lines[len(lines)-5]
			miss_array = miss.strip('\n').split(" ")
			print("Miss Rate :" +miss_array[8])		#MissRate
			MissRate.append(miss_array[8])
			print("\n")

output = open('data.xls','w',encoding='gbk')
output.write('traces\tInstructions\tCPI\tMissRate\n')
for i in range(len(file)):
	output.write(str(file[i]))
	output.write('\t')
	output.write(str(Instructions[i]))
	output.write('\t')
	output.write(str(CPI[i]))
	output.write('\t')
	output.write(str(MissRate[i]))
	output.write('\n')