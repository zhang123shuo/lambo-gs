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
        name_prefix = _(x,4,None).strip(),
        name_en = _(x,20,None).strip(),
        base_secu = _(x,6,None).strip(),
        isin = _(x,12,None).strip(), 
        industry_type = _(x,3,None).strip(),
        currency_type = _(x,2,None).strip(), 
        book_value = float(_(x,7,None)[0:-2]), #special
        total_issue = _(x,12,int),
        free_issue = _(x,12,int),
        pre_profit = _(x,9),
        cur_profit = _(x,9),
        fund_acc_net = _(x,9),
        handle_rate = _(x,7),
        stamp_rate = _(x,7),
        transfer_rate = _(x,7),
        ipo_date = _(x,8),
        bond_interest_date = _(x,8),
        due_date = _(x,8),
        tx_unit = _(x,4,int),
        buy_unit = _(x,6,int),
        sell_unit = _(x,6,int),
        share_limit = _(x,9,int),
        price_stalls = _(x,5),
        auction_limit = _(x,7),
        continous_auction_limit = _(x,7),
        auction_limit_type = _(x,1,int),
        price_up_limit = _(x,9),
        price_down_limit = _(x,9),
        price_up_limit_large = _(x,9),
        price_down_limit_large = _(x,9),
        equ_ratio = _(x,5),
        equ_ratio_mortgage = _(x,5),
        status_margin_money = _(x,1,None),
        status_margin_secu = _(x,1,None),
        status_exponent = _(x,1,None),
        status_mkt_maker = _(x,1,None), 
        mkt_code = _(x,2,None).strip(),
        secu_type = _(x,4,None).strip(),
        status_secu = _(x,1,None),
        status_tx = _(x,1,None),
        status_tx_phase = _(x,1,None),
        status_stopped = _(x,1,None),
        status_margin = _(x,1,None)
    )
    
#===========================================================================
block_size = 302
first_record_offset = 0x7f0
current_offset = 0

import time
start = time.time()
hq = open('dbf/SJSXXN.DBF','rb')
hq.seek(first_record_offset)
count = 0 

while True: 
    try:
        x = hq.read(block_size)  
        if x is None or len(x)==0: break 
        res = parse(x)  
        print res 
        count += 1  
    except Exception,e: 
        break 
    
end = time.time()
print count,(end-start)    
