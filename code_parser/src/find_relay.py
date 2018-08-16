import sys
import re
import string
relay_patten ='[a-zA-Z_]+::\?relay'


fileopen = open('..\\SimpleBLEPeripheral.map','r')


funct_dic ={'backman':0}


lines = fileopen.readlines()

relay_ary=[]

for line in lines:
	relay_funct= re.search(relay_patten,line)
	if relay_funct :
		s = relay_funct.start()
		e = relay_funct.end()
		relay_ary.append(line[s:e])

relay_ary = list (set(relay_ary))
relay_ary.sort()






ta = string.maketrans(':',' ')

i=0

origin_ary=[]
for obj in relay_ary :
	origin_funct=''
	origin_funct=obj.translate(ta)
	origin_funct=origin_funct.replace("  ?relay",'')
	origin_ary.append(origin_funct)

	

#scan origin function address




for obj in origin_ary:
	pt_nextline = 0
	find =0
	
	for line in lines:	
		funct = re.search(obj,line)

		
		
		#find index
		pt_nextline+=1
		
		if funct :
		#same line
			fe=funct.end()
		
			rest_line = line[fe+1:]
			pos = re.search('[0-9A-F]{8}',rest_line);
			
			if pos :
				s = pos.start()
				e = pos.end()
				funct_dic[obj]= rest_line[s:e]					
				print obj
				print rest_line[s:e]	
				find=1
		
		
		 
		#second line
			
			if find ==0 :
				pos = re.search('[0-9A-F]{8}',lines[pt_nextline]);				
				if pos :
					s = pos.start()
					e = pos.end()
					funct_dic[obj]= lines[pt_nextline][s:e]
					print obj
					print lines[pt_nextline][s:e]	
					find=1
						
			if find==1:
				break

	if find ==0 :
		funct_dic[obj]='NONE'

















#scan relay_address  using append

for obj in origin_ary:
	pt_nextline = 0
	find =0
	for line in lines:	
		funct = re.search(obj+'::\?relay',line)
		
		
		#find index
		pt_nextline+=1
		
		if funct :
		#same line
			fe=funct.end()	
			
			rest_line = line[fe+1:]
			pos = re.search('[0-9A-F]{8}',rest_line);
			if pos :
					s = pos.start()
					e = pos.end()
					funct_dic[obj+'::?relay']= rest_line[s:e]
					
					print obj+'::?relay'
					print rest_line[s:e]	
					find=1
		
		
		 
		#second line
			
			if find ==0 :
				pos = re.search('[0-9A-F]{8}',lines[pt_nextline]);	
			
				if pos :
						s = pos.start()
						e = pos.end()
						funct_dic[obj+'::?relay']= lines[pt_nextline][s:e]
						print obj+'::?relay'
						print lines[pt_nextline][s:e]	
						find=1
						
			if find==1:
				break
	
		
	if find ==0 :
		print 'NONE'

		
		





		
#print funct_dic














