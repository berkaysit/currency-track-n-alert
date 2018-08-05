import os
import csv 
cred_detail = []
##os.chdir("Folder where the csv file is stored")
for row in csv.reader(open("pass.csv","rt", encoding='UTF-8')):       
        cred_detail.append(row)

print(cred_detail[0][0])
print(cred_detail[1][0])
print(cred_detail[2][0])
print(cred_detail[3][0])

print(cred_detail[0][1])
print(cred_detail[1][1])
print(cred_detail[2][1])
print(cred_detail[3][1])
print(cred_detail[4][1])


