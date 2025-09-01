import numpy as np
import pandas as pd


def o_c_return_calc(data):
    
    data['o_c'] = (data['Open']/data['Close'])-1
    o_c = data['o_c'].dropna()
    
    # Close Return Calculations
    avg_ret = o_c.mean() # Average total daily Return 
    std = o_c.std() # Deviation From the Mean
    
    total_count = o_c.count() # total count of all data points
    
    pos_count = (o_c > 0).sum() # positive data points
    neg_count = (o_c < 0).sum() # negative data points
    
    pos_perc = (pos_count / total_count)*100  # % Of positive Days
    neg_perc = (neg_count / total_count)*100  # % Of negative Days 
    
    daily_pos_mean = data.loc[data['o_c']> 0, 'o_c'].mean() # Average of only Positive Return 
    daily_neg_mean = data.loc[data['o_c']< 0, 'o_c'].mean() # Average of only Negative Returns 
    
    pos_adj_freq = daily_pos_mean * pos_perc # Adjusted Daily positive Return
    neg_adj_freq = daily_neg_mean * neg_perc # Adjusted Daily negative Return
    
    # Standard Deviation Calculations for Close Returns for each Bound
    upper1 = avg_ret + 1 * std
    lower1 = avg_ret - 1 * std
    count_1 = data[(data['o_c'] >= lower1) & (data['o_c'] <= upper1)].shape[0]
    prc_count_1 = count_1 / total_count

    upper2 = avg_ret + 2 * std
    lower2 = avg_ret - 2 * std
    count_2 = data[(data['o_c'] >= lower2) & (data['o_c'] <= upper2)].shape[0]
    prc_count_2 = count_2 / total_count

    upper3 = avg_ret + 3 * std
    lower3 = avg_ret - 3 * std
    count_3 = data[(data['o_c'] >= lower3) & (data['o_c'] <= upper3)].shape[0]
    prc_count_3 = count_3 / total_count
    
             # Close data table
    o_c_stats_data = [
            # Positive Label
        {"Label": "Positive",
            "Mean": f"{daily_pos_mean:.2%}",
            "Count": pos_count,
            "Frequency %": f"{pos_perc:.2f}%",
            "Adj Return": f"{pos_adj_freq:.2f}%"},
        
        # Negative Label
        {"Label": "Negative",
            "Mean": f"{daily_neg_mean:.2%}",
            "Count": neg_count,
            "Frequency %": f"{neg_perc:.2f}%",
            "Adj Return": f"{neg_adj_freq:.2f}%"},
        ]
    
    o_c_stats_columns = [
        {"name": "", "id": "Label"},
        {"name": "Mean", "id": "Mean"},
        {"name": "Count", "id": "Count"},
        {"name": "Frequency %", "id": "Frequency %"},
        {"name": "Adj Return", "id": "Adj Return"}
        ]
    
    # Table 2 data
    o_c_std_data = [
        # Positive Label
        {"Label": "Std_1", "Upper Bound": f"{upper1:.2%}", "Lower Bound": f"{lower1:.2%}","Count":f"{count_1}","Count %":f"{prc_count_1:.2%}"},
        {"Label": "Std_2", "Upper Bound": f"{upper2:.2%}", "Lower Bound": f"{lower2:.2%}","Count":f"{count_2}","Count %":f"{prc_count_2:.2%}"},
        {"Label": "Std_3", "Upper Bound": f"{upper3:.2%}", "Lower Bound": f"{lower3:.2%}","Count":f"{count_3}","Count %":f"{prc_count_3:.2%}"},
    ]

    o_c_std_columns = [
        {"name": "", "id": "Label"},
        {"name": "Upper Bound", "id": "Upper Bound"},
        {"name": "Lower Bound", "id": "Lower Bound"},
        {"name": "Count", "id": "Count"},
        {"name": "Count %", "id": "Count %"},
    ]

    return {
        "o_c": o_c,
        "o_c_stats_data": o_c_stats_data,
        "o_c_stats_columns": o_c_stats_columns,
        "o_c_std_data": o_c_std_data,
        "o_c_std_columns": o_c_std_columns
    }