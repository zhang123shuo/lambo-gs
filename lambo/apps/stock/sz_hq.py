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
        name = _(x,8,None).decode('gbk').strip(),
        closed = _(x,9),
        open = _(x,9),
        match_price = _(x,9),
        match_qty = _(x,12,int),
        match_value = _(x,17),
        match_tx = _(x,9,int),
        match_price_max = _(x,9),
        match_price_min = _(x,9),
        pe1 = _(x,7),
        pe2 = _(x,7),
        price_delat1 = _(x,9),
        price_delat2 = _(x,9),
        contract_holds = _(x,12,int),
        sell5_price = _(x,9),
        sell5_qty = _(x,12,int),
        sell4_price = _(x,9),
        sell4_qty = _(x,12,int),
        sell3_price = _(x,9),
        sell3_qty = _(x,12,int),
        sell2_price = _(x,9),
        sell2_qty = _(x,12,int),
        sell1_price = _(x,9),
        sell1_qty = _(x,12,int),
        
        buy1_price = _(x,9),
        buy1_qty = _(x,12,int),
        buy2_price = _(x,9),
        buy2_qty = _(x,12,int),
        buy3_price = _(x,9),
        buy3_qty = _(x,12,int),
        buy4_price = _(x,9),
        buy4_qty = _(x,12,int),
        buy5_price = _(x,9),
        buy5_qty = _(x,12,int)
    )
#===========================================================================
block_size = 352
first_record_offset = 0x5e2
current_offset = 0
 
    
import time
start = time.time()
hq = open('dbf/SJSHQ.DBF','rb')
hq.seek(first_record_offset)
count = 0

while True:
    try:
        x = hq.read(block_size)  
        if x is None: break 
        res = parse(x) 
        print res.name,res
        count += 1
    except: 
        break
    
end = time.time()
print count,(end-start)    
