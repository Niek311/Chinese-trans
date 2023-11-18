import re,os
from tqdm import tqdm
from pypinyin.contrib.tone_convert import to_tone

path=os.path.abspath('create-database\cedict_1_0_ts_utf-8_mdbg.txt')
opath=os.path.abspath('create-database\cedict_1_0_ts_utf-8_mdbg.csv')

with open(path, 'r',encoding='utf-8-sig') as file:
    with open(opath, 'w',encoding='utf-8-sig') as ofile:
        lines = file.readlines()
        for line in tqdm(lines):
            a=[i+1 for i,x in enumerate(line) if x=='[']
            b=[i for i,x in enumerate(line) if x==']']
            c=[line[a[i]:b[i]] for i in range(len(a))]

            for i in range(len(c)):
                b=list(c[i].split(" "))
                e= ''.join(to_tone(i)+' ' if index != (len(b)-1) else to_tone(i) for index,i in enumerate(b)  )
                f= ''.join((i)+' ' if index != (len(b)-1) else i for index,i in enumerate(b)  )
                line=re.sub(f,e,line)

            line = re.sub(",",";",line)
            line = re.sub("\s",",",line,2)
            line = re.sub(",,",",",line)
            line = re.sub("] ","],",line,1)
            ofile.write(line.lower())

