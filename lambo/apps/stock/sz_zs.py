#coding=utf-8 
class _dict(dict):
    """A dict that allows for object-like property access syntax."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)
def _(hq,n,t=float):
    global current_offset 
    res = hq[current_offset:current_offset+n] 
    current_offset += n
    if t is None: return res 
    return t(res)

def parse(x):
    global current_offset
    current_offset = 0
    return _dict(
        code = _(x,6,None),
        name = _(x,12,None).decode('gbk').strip(),
        name_en = _(x,20,None).strip(),
        closed = _(x,11),
        open = _(x,11),
        highest = _(x,11),
        lowest = _(x,11),
        latest = _(x,11),
        match_qty = _(x,12,int),
        match_value = _(x,17),
    )
#===========================================================================
block_size = 123
first_record_offset = 0x162
current_offset = 0
 
    
import time
start = time.time()
hq = open('dbf/SJSZS.DBF','rb')
hq.seek(first_record_offset)
count = 0

while True:
    try:
        x = hq.read(block_size)  
        if x is None: break 
        res = parse(x)
        print res.name,res 
        count += 1
    except Exception,e:  
        break
    
end = time.time()
print count,(end-start)    
