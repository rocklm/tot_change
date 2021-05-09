''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Script Name: 
create % changes on time series data

Purpose:
create % changes of two dates in a time series data


Notes:
(1) functions (add_months and per_change) feed into the main function tot_change
(2) tot time on time change
(3) tot_change assumes your periods are month end dates (last day of month)
    can be altered in the for loop at line 100


Changes:

Name            Date            Version         Change
Lee Rock        08/05/2021      v1.0.0          initial version
Lee Rock        08/05/2021      v1.0.1          fixed typos

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                    start of script
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import modules
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''
#modules
import pandas as pd
import datetime as dt
from dateutil.relativedelta import *
import random

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
sub functions - used in main function (tot_change)
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''
#function to add or subract months from a date
#to subract months use "-increment"
#function will work bewteen years
def add_months(dte, increment):
   
   #dte = input date (date data type)
   #increment = the number of months to add/subtract from input date (int)

      return dte + relativedelta(months = increment)

#functionn to calulate the percentage change with the old value as the denominator
#if_zero used to assign a value to division by zero cases e.g 0, 123, 999 -1 etc
def per_change(new_val, old_val, div_zero = 0, rounded = 2):

    #new val = most recent value (float)
    #old_val = previous value (float)
    #if_zero = value if denominator i.e. old value is null or 0 (float)
    #rounded = the mound of decimals to round to (int)

    if old_val == None or old_val == 0:
         delta = div_zero
    else:
        delta = (new_val - old_val)/old_val

    return round(delta, rounded)

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
main function - for users to call
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''
 
#function to get the time on time change in a series
#uses add_months and per_change functions created previously
#this function assumes period dates are monthly (last day of month)
def tot_change(data, date_field, value_field, look_back_mth_num, div_zero = 0):

    #data = input dataset (object)
    #date_field = name of the date field (string)
    #value_field = name of the value field to create deltas (string)
    #look_back_mth_num = number of months to look back for each period (negative int)
    #div_zero = value if denominator i.e. old value is null or 0 (float)

    #initialise list to store deltas
    deltas = []

    #for each record in the series
    for x in range(len(data)):
        #identify the current date of the ith iteration
        cur_date = data[date_field].iloc[x]
        #identify the previous date if look_back_mth_num is subtracted
        #using relativedelta(day=31) ensure the lookback date is converted to the last day of that month
        old_date = add_months(cur_date, look_back_mth_num) + relativedelta(day=31)
        #get the values of the current date 
        cur_val = data[value_field].iloc[x]
        old_val = data.loc[data[date_field] == old_date, value_field]

        #if the old value is null or zero assign the div_zero value
        #by default this will be zero
        if old_val.empty:
            old_val = div_zero
        else:
            old_val = old_val.item()

        deltas.append(per_change(cur_val, old_val))
       
    return deltas

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
sense checking and testing/usage example
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

if __name__ == '__main__':
    #dummy data
    my_date = dt.datetime.strptime('2021-05-31', '%Y-%m-%d').date()
    date_range = [add_months(my_date, x *-1) for x in range(36)]
    val = [random.randint(5,500) for _ in range(len(date_range))]
    df = pd.DataFrame()
    df['PERIOD_DATE'] = date_range
    df['VAL'] = val
    df.sort_values(by=['PERIOD_DATE'], inplace=True )

    #run function and add to existing dataframe
    df['YOY_DELTA'] = tot_change(df,'PERIOD_DATE', 'VAL', -11)
    #print dummy dataframe for testing
    df

    ''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                    end of script
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''



    


