# This code is used for complete implementaion of CGFL technique.
import sys
import time
from datetime import datetime
start_time=datetime.now()
import pandas as pd
import numpy as np
import math
import os
import csv


cwd =os.getcwd()
version=cwd.split("/")[-1]
program_name=cwd.split("/")[-2]
print(cwd)
p=0
i=-1
while i>= (-len(cwd)) :
	if cwd[i]=='/' :
		p=p+1
	if p==2 :
		break
	i=i-1
str_cwd=cwd[:i]
print(str_cwd)
f_l=0

start_time=datetime.now()

with open('faultyLine.txt') as f:
    f_l = f.readline()

print("**************")
print(f_l)
print("**************")

f_l=int(f_l)
df_train=pd.read_csv('statementResult.csv')

#training output dataset
y = np.array([df_train['Result']]).T
y=y.tolist()
#print y

#training input dataset
df_train.drop(['Result'],1 , inplace=True)
t_in = df_train.values.tolist()
x = np.array(t_in)
x=x.tolist()
#print len(y[0])
total_failed=np.count_nonzero(y)
total_passed=len(y)-total_failed



failed_tcn={}
suspicious=[]
#print len(y)
#print len(x[0])
#print total_passed,total_failed


for i in range(0,len(x[0])):
	nsuccess=0
	nfailure=0
	for j in range(0,len(y)):
		#print x[j][i],y[j][0]
		if x[j][i]==1 and y[j][0]==0:
			nsuccess=nsuccess+1
		elif x[j][i]==1 and y[j][0]==1:
			nfailure=nfailure+1
	#print(nfailure)
	if i==f_l:
		my_key=nfailure
	
		
	if (nfailure+nsuccess)!=0 and (len(y)- nfailure-nsuccess)!=0:
		pfe=float(nfailure)/float(nfailure+nsuccess)
		pef=float(nfailure)/float(total_failed)
		pep=float(nsuccess)/float(total_passed)
		ppn=float(total_passed-nsuccess)/float(len(y)- nfailure-nsuccess)
		if pfe==0 or ppn==0 :
			sus_score=-999999
			suspicious.append(sus_score)
			print(str(i)+"   "+str(sus_score))
		elif pfe!=0 and ppn!=0 :
			sus_score=pfe+pef+ppn
			suspicious.append(sus_score)
			print(str(i)+"   "+str(sus_score))
	else :
		sus_score=-999999
		suspicious.append(sus_score)
		print(str(i)+"   "+str(sus_score))

	
	if nfailure not in failed_tcn:
		failed_tcn[nfailure]=[]
	failed_tcn[nfailure].append([i,sus_score])

#print(failed_tcn)
#print(failed_tcn.keys())
length_dict = {key: len(value) for key, value in failed_tcn.items()}
#print(length_dict)
#print("*****************************")
#print(failed_tcn.get(my_key))
#print(type(failed_tcn.get(my_key))) 
def sortSecond(val): 
    return val[1]
#print("*****************************")
list1 = failed_tcn.get(my_key)
# sorts the array in descending according to 
# second element 
list1.sort(key = sortSecond, reverse = True) 
#print(list1) 
#=================================================
# To compute the number of elements needed to be searched before entring to the group of my key
tot_search=0
#print("in between search items")
for se in range(my_key+1, len(length_dict)):
	tot_search=tot_search+length_dict.get(se,int(0))
d = {}
for i in range(0,len(list1)):
	key = float(list1[i][1])
	if key not in d:
		d[key] = []
	d[key].append(list1[i][0])


ct1=0
ct2=0
ct3=0
fct=0
print("Faulty line:"+str(f_l))
for i in sorted(d):
	#print (i,len(d[i]))
	if f_l not in d[i] and fct==0:
		ct1=ct1+len(d[i])
	elif f_l not in d[i] and fct==1:
		ct3=ct3+len(d[i])
	else: 
		fct=1
		ct2=len(d[i])
print("We have to search "+str(tot_search+ct3+1)+" to "+str(tot_search+ct3+ct2))



end_time=datetime.now()
csvfile=open(str_cwd+"/new_grp.csv", "a+")
spamwriter1 = csv.writer(csvfile, delimiter=',')
stmt_complex=[]
stmt_complex.append(program_name);
stmt_complex.append(str(version));
#stmt_complex.append(str(sys.argv[1]));
stmt_complex.append(f_l);
stmt_complex.append(tot_search+ct3+1);
stmt_complex.append(tot_search+ct2+ct3);
stmt_complex.append(start_time);
stmt_complex.append(end_time);
stmt_complex.append(end_time-start_time);
stmt_complex.append(total_passed);
stmt_complex.append(total_failed);
spamwriter1.writerow(stmt_complex);


