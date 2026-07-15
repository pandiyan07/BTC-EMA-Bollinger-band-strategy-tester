import pandas as pd
import pandas_ta as ta
import yfinance as yf
import time
import re


def TRADER(df, price_data, date_time_list):
    # Trading conditions
    long_trade_active = False
    short_trade_active = False
    Ltrade = []
    Lt = 1
    Strade = []
    St = 1
    
    
    long_trade = {}
    long_entry_price = []
    long_exit_price = []
    long_close_price = []
    long_bb_banwidth = []
    long_p_and_l = []
    long_date_time = []
    bt_ema_hl2 = []
    long_trade_sl = []
    bt_candle_open = []
    bt_candle_close = []
    bt_closeexit_ema_hl2 = []
    bt_closeexit_candle_open = []
    bt_closeexit_candle_close = []
    
    
    short_trade = {}
    st_ema_hl2 = []
    st_candle_open = []
    st_candle_close = []
    st_closeexit_ema_hl2 = []
    short_entry_price = []
    short_exit_price = []
    short_close_price = []
    short_bb_banwidth = []
    short_p_and_l = []
    short_date_time = []
    short_trade_sl = []
    st_closeexit_candle_open = []
    st_closeexit_candle_close = []
    
    
    bollinger_bandwidth = 60
    long_trade_max_profit = 0
    short_trade_max_profit = 0
    
    for index, row in df.iterrows():
        if not long_trade_active and not short_trade_active:
            #Long trade ENTRY
            #if (row.iloc[7] - row.iloc[5] >= bollinger_bandwidth and row['open'] > row.iloc[6] and row['close'] > row.iloc[6]):
            if (row.iloc[2] - row.iloc[0] >= bollinger_bandwidth and row['open'] > row.iloc[1] and row['close'] > row.iloc[1]):
                long_trade_active = True
                lep = round(price_data[index],0)
                long_entry_price.append(lep)
                lep_list_len = len(long_entry_price)
                long_date_time.append(date_time_list[index])
                #long_bb_banwidth.append(round(row.iloc[8] - row.iloc[5],0))
                long_bb_banwidth.append(round(row.iloc[2] - row.iloc[0],0))
                bt_ema_hl2.append(row.iloc[1])
                bt_candle_open.append(row['open'])
                bt_candle_close.append(row['close'])
                
                
            #Short trade ENTRY
            #elif (row.iloc[7] - row.iloc[5] >= bollinger_bandwidth and row['open'] < row.iloc[6] and row['close'] < row.iloc[6]):
            elif (row.iloc[2] - row.iloc[0] >= bollinger_bandwidth and row['open'] < row.iloc[1] and row['close'] < row.iloc[1]):
                short_trade_active = True
                sep = round(price_data[index],0)
                short_entry_price.append(sep)
                sep_list_len = len(short_entry_price)
                short_date_time.append(date_time_list[index])
                #short_bb_banwidth.append(round(row.iloc[8] - row.iloc[5],0))
                short_bb_banwidth.append(round(row.iloc[2] - row.iloc[0],0))
                st_ema_hl2.append(row.iloc[1])
                st_candle_open.append(row['open'])
                st_candle_close.append(row['close'])
        
        
        #Long trade CLOSE
        #if (long_trade_active and row['open'] < row.iloc[6] and row['close'] < row.iloc[6]):
        if (long_trade_active and row['open'] < row.iloc[1] and row['close'] < row.iloc[1]):
            long_trade_active = False
            long_close_price.append(round(price_data[index],0))
            long_exit_price.append(0)
            p_and_l = price_data[index] - lep
            long_p_and_l.append(round(p_and_l,0))
            Ltrade.append(Lt)
            Lt += 1
            bt_closeexit_ema_hl2.append(row.iloc[1])
            bt_closeexit_candle_open.append(row['open'])
            bt_closeexit_candle_close.append(row['close'])
        
        
        # Long SL EXIT
        if (long_trade_active):
            if long_trade_max_profit == 0:
                long_trade_max_profit = price_data[index]
            else:
                if price_data[index] > long_trade_max_profit:
                    long_trade_max_profit = price_data[index]
                else:
                    long_profit = (long_trade_max_profit - long_entry_price[lep_list_len-1])
                    ltsl = long_entry_price[lep_list_len-1]  + (long_profit * 0.9)
                    if ltsl > price_data[index]:
                        long_trade_active = False
                        long_exit_price.append(round(price_data[index],0))
                        long_close_price.append(0)
                        p_and_l = price_data[index] - lep
                        long_p_and_l.append(round(p_and_l,0))
                        Ltrade.append(Lt)
                        long_trade_max_profit = 0
                        Lt += 1
                        bt_closeexit_ema_hl2.append(row.iloc[1])
                        bt_closeexit_candle_open.append(row['open'])
                        bt_closeexit_candle_close.append(row['close'])
                        long_trade_sl.append(f'{ltsl}({price_data[index]})')

        
        
        #Short trade CLOSE
        #if (short_trade_active and row['open'] > row.iloc[6] and row['close'] > row.iloc[6]):
        if (short_trade_active and row['open'] > row.iloc[1] and row['close'] > row.iloc[1]):
            short_trade_active = False
            short_close_price.append(round(price_data[index],0))
            short_exit_price.append(0)
            p_and_l = sep - price_data[index]
            short_p_and_l.append(round(p_and_l,0))
            Strade.append(St)
            St += 1
            st_closeexit_ema_hl2.append(row.iloc[1])
            st_closeexit_candle_open.append(row['open'])
            st_closeexit_candle_close.append(row['close'])
        
        
        
        # Short SL EXIT
        if (short_trade_active):
            if short_trade_max_profit == 0:
                short_trade_max_profit = price_data[index]
            else:
                if price_data[index] < short_trade_max_profit:
                    short_trade_max_profit = price_data[index]
                else:
                    short_profit = (short_entry_price[sep_list_len-1] - short_trade_max_profit)
                    stsl = short_entry_price[sep_list_len-1]  - (short_profit * 0.9)
                    if stsl < price_data[index]:
                        short_trade_active = False
                        short_exit_price.append(round(price_data[index],0))
                        short_close_price.append(0)
                        p_and_l = sep - price_data[index]
                        short_p_and_l.append(round(p_and_l,0))
                        Strade.append(St)
                        St += 1
                        st_closeexit_ema_hl2.append(row.iloc[1])
                        st_closeexit_candle_open.append(row['open'])
                        st_closeexit_candle_close.append(row['close'])
                        short_trade_sl.append(f'{stsl}({price_data[index]})')


    if len(long_entry_price) > len(long_exit_price):
        Ltrade.append(len(long_entry_price))
        long_exit_price.append(0)
        long_close_price.append(0)
        long_p_and_l.append(0)
        bt_ema_hl2.append(0)
        bt_candle_open.append(0)
        bt_candle_close.append(0)
        bt_closeexit_ema_hl2.append(0)
        bt_closeexit_candle_open.append(0)
        bt_closeexit_candle_close.append(0)
    
    if len(short_entry_price) > len(short_exit_price):
        Strade.append(len(short_entry_price))
        short_exit_price.append(0)
        short_close_price.append(0)
        short_p_and_l.append(0)
        st_ema_hl2.append(0)
        st_candle_open.append(0)
        st_candle_close.append(0)
        st_closeexit_ema_hl2.append(0)
        st_closeexit_candle_open.append(0)
        st_closeexit_candle_close.append(0)
    
    long_loss = []
    short_loss = []
    long_profit = []
    short_profit = []
    
    for l in long_p_and_l:
        if l < 0:
            long_loss.append(l)
        else:
            long_profit.append(l)
    
    for s in short_p_and_l:
        if s < 0:
            short_loss.append(s)
        else:
            short_profit.append(s)
    
    L_border_line = []
    for i in range(len(Ltrade)):
        L_border_line.append('|')
    
    S_border_line = []
    for i in range(len(Strade)):
        S_border_line.append('|')
    
    long_trade.update({'Lng trd no': list(Ltrade)})
    #long_trade.update({'Datetime': list(long_date_time)})
    long_trade.update({'Entry price': list(long_entry_price)})
    long_trade.update({'Entry EMA': list(bt_ema_hl2)})
    long_trade.update({'Entry candle O': list(bt_candle_open)})
    long_trade.update({'Entry candle C': list(bt_candle_close)})
    long_trade.update({'[': list(S_border_line)})
    long_trade.update({']': list(S_border_line)})
    long_trade.update({'Close price': list(long_close_price)})
    long_trade.update({'SL': list(long_trade_sl)})
    long_trade.update({'SL Exit price': list(long_exit_price)})
    long_trade.update({'Exit EMA': list(bt_closeexit_ema_hl2)})
    long_trade.update({'Exit candle O': list(bt_closeexit_candle_open)})
    long_trade.update({'Exit candle C': list(bt_closeexit_candle_close)})
    long_trade.update({'<': list(L_border_line)})
    long_trade.update({'P&L': list(long_p_and_l)})
    long_trade.update({'>': list(L_border_line)})
    long_trade.update({'BB bandwidth': list(long_bb_banwidth)})
    
    
    short_trade.update({'Shrt trd no': list(Strade)})
    #short_trade.update({'Datetime': list(short_date_time)})
    short_trade.update({'Entry price': list(short_entry_price)})
    short_trade.update({'Entry EMA': list(st_ema_hl2)})
    short_trade.update({'Entry candle O': list(st_candle_open)})
    short_trade.update({'Entry candle C': list(st_candle_close)})
    short_trade.update({'[': list(S_border_line)})
    short_trade.update({']': list(S_border_line)})
    short_trade.update({'Close price': list(short_close_price)})
    short_trade.update({'SL': list(short_trade_sl)})
    short_trade.update({'SL Exit price': list(short_exit_price)})
    short_trade.update({'Exit EMA': list(st_closeexit_ema_hl2)})
    short_trade.update({'Exit candle O': list(st_closeexit_candle_open)})
    short_trade.update({'Exit candle C': list(st_closeexit_candle_close)})
    short_trade.update({'<': list(S_border_line)})
    short_trade.update({'P&L': list(short_p_and_l)})
    short_trade.update({'>': list(S_border_line)})
    short_trade.update({'BB bandwidth': list(short_bb_banwidth)})
    
    
    long_trade_df = pd.DataFrame(long_trade)
    long_trade_df = long_trade_df.reset_index(drop=True)
    long_trade_df = long_trade_df.set_index('Lng trd no')
    
    short_trade_df = pd.DataFrame(short_trade)
    short_trade_df = short_trade_df.reset_index(drop=True)
    short_trade_df = short_trade_df.set_index('Shrt trd no')
    
    
    
    plt_df = long_trade_df[long_trade_df['P&L'] > 0]
    plt_df = plt_df.sort_values(by='P&L', ascending=False)
    print ('\n\n')
    print ("        >>>>>           Profitable Long trades            <<<<<")
    print (plt_df)
    
    '''
    llt_df = long_trade_df[long_trade_df['P & L'] <= 0]
    llt_df = llt_df.sort_values(by='P & L', ascending=True)
    print ('\n\n')
    print ("        >>>>>           Loss Long trades            <<<<<")
    print (llt_df)
    '''
    
    pst_df = short_trade_df[short_trade_df['P&L'] > 0]
    pst_df = pst_df.sort_values(by='P&L', ascending=False)
    print ('\n\n')
    print ("        >>>>>           Profitable Short trades           <<<<<")
    print (pst_df)
    '''
    lst_df = short_trade_df[short_trade_df['P & L'] <= 0]
    lst_df = lst_df.sort_values(by='P & L', ascending=True)
    print ('\n\n')
    print ("        >>>>>           Loss Short trades            <<<<<")
    print (lst_df)
    '''
    
    print ('\n\n')
    print (f"Net profit Long trade is = ({sum(long_profit)}) + ({sum(long_loss)}) = ",sum(long_p_and_l))
    print ('Gross Long trade profit is = ',sum(long_profit))
    print ("Gross Long trade loss is = ",sum(long_loss))
    print ('Total Long trades taken =',len(plt_df)+len(llt_df))
    print ('Total number of Long profit trades =',len(plt_df))
    print ('Total number of Long loss trades =',len(llt_df))
    
    print ('\n\n')
    print (f"Net profit Short trade is = ({sum(short_profit)}) + ({sum(short_loss)}) = ",sum(short_p_and_l))
    print ('Gross Short trade profit is = ',sum(short_profit))
    print ("Gross Short trade loss is = ",sum(short_loss))
    print ('Total Short trades taken =',len(plt_df)+len(lst_df))
    print ('Total number of Short profit trades =',len(pst_df))
    print ('Total number of Short loss trades =',len(lst_df))
    
    print ('\n\n')
    print (f"Total net profit - ({sum(long_p_and_l)}) + ({sum(short_p_and_l)}) = ",sum(long_p_and_l)+sum(short_p_and_l))
    print ('Total trades taken = ',len(long_trade_df)+len(short_trade_df))
    print ('Percentage profitable = ',((len(plt_df) + len(pst_df)) / (len(plt_df) + len(pst_df) + len(llt_df) + len(lst_df))) * 100 )
    
    
    



def RSI_BOLLINGER_BAND_CALCULATOR(tv_bank_nifty):
    #       include these columns = bt_ema_hl2(bollinger middle band), bt_candle_open(open), bt_candle_close(close), 
    #       bt_exit_ema_hl2(bollinger middle band), bt_exit_candle_open(open), bt_exit_candle_close(close),
    #       st_ema_hl2, st_candle_open, st_candle_close, st_exit_ema_hl2, st_exit_candle_open, st_exit_candle_close



    bollinger_length = 9
    bollinger_std = 2
    '''
    date_time_list = tv_bank_nifty.index.tolist()
    price_data = (tv_bank_nifty['high'] + tv_bank_nifty['low'])/2
    price_data = list(price_data)
    '''
    price_data = [1,2,3,4,5,6,7,60,80,100,120,140,160,180,200,220,240,260,280,260,240,220,200,180,160,140,120,100,80,160]
    supportive_price_data = [1,2,3,4,5,6,7,70,90,110,130,150,170,190,210,230,250,250,230,210,190,170,150,130,110,90,70,50,30,150]
    date_time_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
    
    # Calculate RSI
    #df['RSI'] = ta.rsi(df['Price'], length=rsi_length)
    # Calculate the 5-period EMA of the RSI
    #df['RSI 5 EMA'] = ta.ema(df['RSI'], length=rsi_length)
    #df['Date & Time'] = date_time_list
    
    
    price_df = pd.DataFrame({'Price': price_data})
    bollinger = ta.bbands(price_df['Price'], length=bollinger_length, std=bollinger_std)
    bollinger = bollinger.rename(columns={
        'BBL_9_2.0': 'Bollinger Lower Band',
        'BBM_9_2.0': 'Bollinger Middle Band',
        'BBU_9_2.0': 'Bollinger Upper Band',
        'BBB_9_2.0': 'Bollinger Band Basis',
        'BBP_9_2.0': 'Bollinger Band %B'
    })
    '''
    bollinger_index  = bollinger.index.tolist()
    tv_bank_nifty['index'] = bollinger_index
    tv_bank_nifty = tv_bank_nifty.reset_index(drop=True)
    tv_bank_nifty = tv_bank_nifty.set_index('index')
    tv_bank_nifty['Datetime'] = date_time_list 
    
    bollinger = bollinger.drop(columns=['Bollinger Band Basis'])
    df = pd.concat([tv_bank_nifty,bollinger], axis=1) 
    '''
    df = bollinger
    df['open'] = price_data
    df['close'] = supportive_price_data
    
    
    TRADER(df,price_data,date_time_list)



'''
bank_nifty = yf.download(tickers="^NSEBANK", period="7d", interval="1m")
#print (bank_nifty)
date_time_list = bank_nifty.index.tolist()
'''
from tvDatafeed import TvDatafeed, Interval
tv = TvDatafeed()
RSI_BOLLINGER_BAND_CALCULATOR(0)


def DATA_FETCHER():
    #tv_bank_nifty = tv.get_hist(symbol='BANKNIFTY',exchange='NSE',interval=Interval.in_1_minute,n_bars=10)
    
    def ERROR_DETECTOR(text, word_to_find):
        # Create a regex pattern with word boundaries
        pattern = r"\b{}\b".format(word_to_find)
        # Use re.search() to find the word (case-insensitive by default)
        match = re.search(pattern, text)
        return bool(match)  # Return True/False based on match existence
    
    if ERROR_DETECTOR(str(tv_bank_nifty), None):
        print("Data fetching failed for Retrying in 5 seconds...\n")
        time.sleep(5)  # Introduce a 5-second delay
        DATA_FETCHER()  # Retry the download
    else:
        print("Great..!! The are no ConnectionErrors while fetching the data.")
        tv_bank_nifty = tv_bank_nifty.drop(columns=['symbol', 'volume'])
        print (tv_bank_nifty)
        RSI_BOLLINGER_BAND_CALCULATOR(tv_bank_nifty)

DATA_FETCHER()
