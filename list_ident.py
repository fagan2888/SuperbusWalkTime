f=open('indent_out.csv','r')
lines=f.readlines()
i_list=[]
f=open('ident_list.txt','w')

for line in lines:
    ident=line.split(',')[3].strip()
    if ident not in i_list and ident!='':
        i_list.append(ident)
        f.write(ident+'\n')
f.close()
print i_list
print len(i_list)
