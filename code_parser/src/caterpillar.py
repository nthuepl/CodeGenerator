import h_to_map

import string



		

def spit(fv):
	
	if (h_to_map.conf_dic[fv]&0x01) ==0x01:
		dir_v='direct'
	elif (h_to_map.conf_dic[fv]&0x02) ==0x02:
		dir_v='indirect'
	else:
		dir_v='None'
	if (h_to_map.conf_dic[fv]&0x0c) ==0x0c:
		sk_v="\'XSTACK\',\'ISTACK\'"
	elif (h_to_map.conf_dic[fv]&0x08) ==0x08:
		sk_v='\'ISTACK\''
	elif (h_to_map.conf_dic[fv]&0x04) ==0x04:
		sk_v='\'XSTACK\''
		
	else:
		sk_v='None'
		
	values={'funct':fv,'addr':h_to_map.addr_dic[fv],'bank':h_to_map.bank_dic[fv],'size':h_to_map.size_dic[fv],'dir':dir_v,'stack':sk_v,'rtype':h_to_map.f_o_dic[fv],'ptype':h_to_map.ptype[fv],'pname':h_to_map.pname[fv],'relay':h_to_map.relay_addr_dic[fv]}
	tmp_content = string.Template("""
	'$funct':{
		'address': $addr,
		'relay': $relay,
		'bank': $bank,
		'size': $size,
		'calls': '$dir',
		'stacks': [$stack],
		'returnType': '$rtype',
		'paramTypes': $ptype,
		'paramNames': $pname,
		},			
	""")
	#print (tmp_content.substitute(values))
	return tmp_content.substitute(values)


def output1() :
	str='_map={ '
	for fv in h_to_map.fv_n_ary:
		str+=spit(fv)
	str+=' }'
	#print str
	f=open(r'..\result_2540\dic.py','w')
	f.write(str)

def output2() :
	str='_map={ '
	for fv in h_to_map.fv_n_ary:
		str+=spit(fv)
	str+=' }'
	#print str
	f=open(r'..\result_2541\dic.py','w')
	f.write(str)		
	




#'.\\SimpleBLEPeripheral.map'




ch= int(input("Enter the version of chip:\n1 for cc2540 \n2 for cc2541 \n> "));

fileopen = open(r'..\head_path.txt','r')

lines = fileopen.readlines()



#eat tree
if ch==1:
	h_to_map.eat_map(r'..\..\Device\EcoBT\Project\ble\CodeGenerator\CC2540DB\CC2540\List\SimpleBLEPeripheral.map')
else:
	h_to_map.eat_map(r'..\..\Device\EcoBT\Project\ble\CodeGenerator\CC2541DB\CC2541\List\SimpleBLEPeripheral.map')

for line in lines:
	#print (line)
	h_to_map.eat_head(line[:-1])
	
if ch==1:	
	output1()
else: 
	output2()
print "----------------------------------"
print "            Done!                 "
print "----------------------------------"	

	
# for debug	
#for obj in h_to_map.fv_n_ary:
#	show_result(obj)
		
	


	
	
	
	