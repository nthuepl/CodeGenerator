
#
# file: sdccmapparser.py
#
# this python script to parser sdcc map file to generator *.h header file
# for function address

import sys
import re

L = []

if len(sys.argv) != 4:
	sys.exit("usage: " + sys.argv[0] + """ sdccmapfile.map prefix outfile.h, 
	where sdccmapfile is the map file generated by the sdcc compiler, prefix
	is added in front of all macro names (let's use "MAP_"), and 
	outfile.h is the name of the output file as C header file.""")

try:
	fmap = open(sys.argv[1])
except:
	sys.exit("cannot open sdcc map file "+sys.argv[1]+" for reading")
	
try:
	fh = open(sys.argv[3],'w')
except:
	sys.exit('cannot write to output file '+sys.argv[2])

for line in fmap:
	matchObj = re.match(r'C:\s{3}([0-9a-fA-F]+)\s{2}(\w+)\s+\w+',line)
	if matchObj:
		L.append([ matchObj.group(2)[1:], matchObj.group(1)])
	
fh.write('/*************** SDCC fucntion address ***************/\n')
for (name, address) in L:
	#print name, address
	fh.write('#define %-50s %s\n' % (sys.argv[2]+"_"+name, hex(int(address, 16)) ) )

fmap.close()
fh.close()