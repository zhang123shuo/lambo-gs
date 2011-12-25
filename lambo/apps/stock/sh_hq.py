#coding=utf-8 
class _dict(dict):
    """A dict that allows for object-like property access syntax."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)
        
raw_float = float
raw_int = int
def float(value):
    value = value.replace('-','0')
    return raw_float(value)
def int(value):
    value = value.replace('-','0')
    return raw_int(value)

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
        name = _(x,8,None).decode('gbk').strip(),
        closed = _(x,8),
        open = _(x,8),
        match_value = _(x,12,int),
        match_price_max = _(x,8),
        match_price_min = _(x,8),
        match_price = _(x,8), 
        buy1_price = _(x,8),
        sell1_price = _(x,8),
        match_qty = _(x,10,int),
        pe = _(x,8), 
        
        buy1_qty = _(x,10,int),
        
        buy2_price = _(x,8),
        buy2_qty = _(x,10,int),
        buy3_price = _(x,8),
        buy3_qty = _(x,10,int),
        
        sell1_qty = _(x,10,int),
        
        sell2_price = _(x,8),
        sell2_qty = _(x,10,int),
        sell3_price = _(x,8),
        sell3_qty = _(x,10,int), 
        
        buy4_price = _(x,8),
        buy4qty = _(x,10,int),
        buy5_price = _(x,8),
        buy5_qty = _(x,10,int),
        
        sell4_price = _(x,8),
        sell4_qty = _(x,10,int),
        sell5_price = _(x,8),
        sell5_qty = _(x,10,int), 
    )
#===========================================================================
block_size = 265
first_record_offset = 0x4eb
current_offset = 0
 
    
import time
start = time.time()
hq = open('dbf/show2003.dbf','rb')
hq.seek(first_record_offset)
count = 0 
while True:
    try:
        x = hq.read(block_size)  
        if x is None: break 
        res = parse(x)
        #print res.name,res
        count += 1 
        #if count > 1000: break
    except Exception, e:  
        break
    
end = time.time()
print count,(end-start)    
