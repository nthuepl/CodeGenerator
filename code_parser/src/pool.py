import sys
import re
import string




fileopen = open(r'.\targetmap.map','r')
lines = fileopen.readlines()

syndrome=' ===== '
	
pt_n_line=0

var_dic ={}


for line in lines:
	pt_n_line+=1		
	pat= re.search(syndrome,line)
	if pat:
		var=re.search('[a-zA-Z\_]+',lines[pt_n_line])
		if var:
			addr=re.search('[0-9A-F]{8}',lines[pt_n_line])
			if addr:
				s=var.start()
				e=var.end()
				ss=addr.start()
				ee=addr.end()
				var_dic[ lines[pt_n_line][s:e] ]=lines[pt_n_line][ss:ee]
			