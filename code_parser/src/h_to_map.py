import sys
import re
import string
import rm_comment	
import subprocess
import string
import time
fv_n_ary =[]
f_o_dic={}
f_i_dic={}
addr_dic={}
relay_addr_dic={}
conf_dic={}
bank_dic={}
size_dic={}

ptype={}
pname={}








def eat_map(map_path):

#----------------------------------------------------------------
#          READ map file
#
#----------------------------------------------------------------
	

#s1 name of funct and variable
	fileopen = open(map_path,'r')
	lines = fileopen.readlines()

	
	
	
	syndrome=' ===== '
	
	pt_n_line=0
    
	


	for line in lines:
		pt_n_line+=1
		find=0
		pat= re.search(syndrome,line)
		if pat:
			var=re.search('[0-9a-zA-Z_]+',lines[pt_n_line])
			test=re.search('::?',lines[pt_n_line])
			if var and (not test):
				tmp_p=0
				s=var.start()
				e=var.end()	
				fv_name=lines[pt_n_line][s:e]
				fv_n_ary.append(fv_name)
#---------------bank and size
				bank=re.search('[0-9]',lines[pt_n_line-5])
				if bank:
					s=bank.start()
					e=bank.end()
					bank_dic[fv_name]=lines[pt_n_line-5][s:e]
					#print lines[pt_n_line-5][s:e]
				else:
					bank_dic[fv_name]='None'
				size=re.search('0x[0-9a-zA-Z]+',lines[pt_n_line-4])
				if size:
					s=size.start()
					e=size.end()
					size_dic[fv_name]=lines[pt_n_line-4][s:e]
					#print lines[pt_n_line-4][s:e]
				else:
					size_dic[fv_name]='None'
				
				#print fv_name +' XXX'+lines[pt_n_line]
#---------------#addr
				rest_line = lines[pt_n_line]
				pos = re.search('[0-9A-F]{8}',rest_line);
				if pos :
						s = pos.start()
						e = pos.end()
						
						#relay_addr_ary.append(rest_line[s:e])
						addr_dic[fv_name]='0x'+rest_line[s:e]
						
						#print rest_line[s:e]	
						tmp_p= pt_n_line
						find=1
				#second line
				if find==0 :
					pos = re.search('[0-9A-F]{8}',lines[pt_n_line+1]);	
				
					if pos :
							s = pos.start()
							e = pos.end()
							#relay_addr_ary.append(lines[pt_nextline][s:e])
							addr_dic[fv_name]='0x'+lines[pt_n_line+1][s:e]
							#print obj+'::?relay'
							#print lines[pt_nextline][s:e]	
							find=1
							tmp_p= pt_n_line+1
										
				if find ==0 :
					#print 'NONE-realy'
					addr_dic[fv_name]='None'
				
			# find other setting
			conf_n=0x0
			#print 'CONF!!'
			
			while not re.search('[\*]{40}',lines[tmp_p]) and not re.search('-------------------------------------------------------------------------',lines[tmp_p]) :
				#print "in"
				#direct
				if re.search('direct',lines[tmp_p]):
					conf_n|=0x01
				#indirect
				if re.search('indirect',lines[tmp_p]):
					conf_n|=0x02
				#XSTACK
				if re.search('XSTACK',lines[tmp_p]):
					conf_n|=0x04
				#ISTACK
				if re.search('ISTACK',lines[tmp_p]):
					conf_n|=0x08;
				tmp_p+=1
			conf_dic[fv_name]=conf_n
			#print fv_name
			#print conf_n
	#print 'map (fv,addr,conf) done'	
				
				
				
	
				
				
				
				
				
				
				
				
				
				
				
	
	#s2 addr
	# addr_pat='[0-9A-F]{8}'
	# for obj in fv_n_ary:
		# pt_nextline = 0
		# find =0
		# for line in lines:	
			# funct = re.search(obj,line)
			
			
			#find index
			# pt_nextline+=1
			
			# if funct :
			#same line
				# fe=funct.end()	
				
				# rest_line = line[fe+1:]
				# pos = re.search('[0-9A-F]{8}',rest_line);
				# if pos :
						# s = pos.start()
						# e = pos.end()
						
						#relay_addr_ary.append(rest_line[s:e])
						# addr_dic[obj]=rest_line[s:e]
						#print obj+'::?relay'
						#print rest_line[s:e]	
						# find=1
			
			
			 
			#second line
				
				# if find ==0 :
					# pos = re.search('[0-9A-F]{8}',lines[pt_nextline]);	
				
					# if pos :
							# s = pos.start()
							# e = pos.end()
							#relay_addr_ary.append(lines[pt_nextline][s:e])
							# addr_dic[obj]=lines[pt_nextline][s:e]
							#print obj+'::?relay'
							#print lines[pt_nextline][s:e]	
							# find=1
							
				# if find==1:
					# break
		
			
		# if find ==0 :
			#print 'NONE-realy'
			# addr_dic[obj]='None'
					
					

		
	#----------------------------------------------------------------------------	
	#2

	#relay_addr_ary=[]
	
	
	#s3 relay     too many fv don't have relay!! <----cost time!
	print " too many fv don't have relay!! <----cost time! "
	for obj in fv_n_ary:
		
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
						
						#relay_addr_ary.append(lines[pt_nextline][s:e])
						relay_addr_dic[obj]='0x'+rest_line[s:e]
						#print obj+'::?relay'
						#print lines[pt_nextline][s:e]	
						find=1
						
				if find ==0 :
					pos = re.search('[0-9A-F]{8}',lines[pt_nextline]);	
			
					if pos :
						s = pos.start()
						e = pos.end()
						relay_addr_dic[obj]='0x'+lines[pt_nextline][s:e]
						#print obj+'::?relay'
						#print lines[pt_nextline][s:e]	
						find=1			
							
							
							
							
							
				if find==1:
					break
		
			
		if find ==0 :
			#print 'NONE-realy'
			relay_addr_dic[obj]='None'
		
		
	print 'map relay done'	



def eat_head(h_path):

	#funct_tuple={'name','o_t','i_t','address'}



	#funct_name

	#f_n_pat = '[a-zA-Z]+\('

	




	#--------------------------------------

	#fileopen = open(h_path,'r')

	#lines = fileopen.readlines()




	#s1
	# for line in lines:
		# funct_name= re.search(f_n_pat,line)
		# if funct_name:
			# s=funct_name.start()
			# e=funct_name.end()
			#print line[s:e-1]
			# f_n_ary.append(line[s:e-1])
					
			
			
	#----------------------------------------------------------		
			
			
	#function output type

	#f_o_pat='[a-zA-Z] '+f_n
		

	#f_o_ary=[]
	
	stream = open(h_path,'r')
	print h_path
	fstr = stream.readlines()
	tmp_stream=open(r'.\tmp.h','w')

	for str in fstr:
		str=str.replace(r'#include','//')
		tmp_stream.write(str)

	tmp_stream.close()


	subprocess.Popen(r'C:\MinGW\bin\cpp.exe  -fpreprocessed .\tmp.h -o .\tmp2.h')
	subprocess.Popen(r'C:\Program Files\IAR Systems\Embedded Workbench 6.4\8051\bin\icc8051.exe .\tmp.h --preprocess tmp2.h')
	
	time.sleep(3)
	
	fileopen = open(r'.\tmp2.h','r')
	lines = fileopen.readlines()
	
	
	
	
	
	#fileopen = open(h_path,'r')
	#f_c = rm_comment.remove_comments(fileopen.read())
	#lines=f_c.splitlines(True)
	
	
	
	
	#s4 rtype/ptype
	
	for name in fv_n_ary:
		i_type_ary=[]
		i_name_ary=[]
		find=0
		f_o_pat=name+'\s*\('
		for line in lines:
			f_o_t= re.search(f_o_pat,line)
			if f_o_t:
			#rtype
				
				e=f_o_t.end()
				s=f_o_t.start()
				#print line[:e-1]
				#f_o_ary.append(line[s:e-len(name)])
				#f_o_dic[name]=line[s:e-len(name)]
				w_list=line[:e-1].split()
				if len(w_list)==2:
					if(line[s-1]=='*'):
						f_o_dic[name]=w_list[0]+'*'
					else:
						f_o_dic[name]=w_list[0]
							
				else:
					if(line[s-1]=='*'):
						f_o_dic[name]=w_list[1]+'*'
					else:
						f_o_dic[name]=w_list[1]
			#ptype
				print line[e:]
				w_list=line[e:].split()
				i_index=0
				f_unsigned=0
				
				for obj in w_list:
					f_drop=0
					tmp_s=[]
					if obj!=');':
					
						
						if obj=="unsigned":
							tmp_s=obj
							f_unsigned=1
						elif obj=="const":
							f_drop=1
						elif obj=="GENERIC":
							f_drop=1
						elif i_index%2==0:
							obj=obj.replace(')','')
							obj=obj.replace(';','')
							obj=obj.replace(',','')
							if obj.find(',')!=-1:
								i_name_ary.append('auto_name')
								i_index=i_index+1
							if(f_unsigned==1):
								obj="unsigned "+obj
								f_unsigned=0
							print obj
							i_type_ary.append(obj)
						else:
							obj=obj.replace(')','')
							obj=obj.replace(';','')
							obj=obj.replace(',','')
							if(obj=='*'):
								obj=obj.replace('*','*auto_name')
							print obj
							i_name_ary.append(obj)
					else:
						break
					if f_unsigned==0 and f_drop==0 :
						i_index=i_index+1
					
				
				
				ptype[name]=i_type_ary
				pname[name]=i_name_ary
				find=1
				break
		if find==0:
			if not(name in f_o_dic):
				f_o_dic[name]='None'
				ptype[name]=[]
				pname[name]=[]
	#------------------------------------------------------------------
			
	#function input type

	#f_i_pat=name+(......)
		

	
	
	

				
	
#-------------------------------------------------		
		
		
		
		
		
		
		
		
	

		
#funct_tuple=('name','output','input','address','relay_addr')		
#funct_tuple_list=[]
#funct_tuple_list.append(funct_tuple)

#i=0
#for name in f_n_ary:
#	funct_tuple= (f_n_ary[i],f_o_ary[i],f_i_ary[i],addr_ary[i],relay_addr_ary[i])
#	funct_tuple_list.append( funct_tuple )
#	i=i+1

	
		
		
		
#for obj in funct_tuple_list:
#	print obj