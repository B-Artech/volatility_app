import numpy as np
import pandas as pd


def h_l_return_calc(data):
    
    data['h_l'] = (data['High']/data['Low'])-1
    h_l = data['h_l'].dropna()
    
    # Close Return Calculations
    avg_ret = h_l.mean() # Average total daily Return 
    std = h_l.std() # Deviation From the Mean
    
    total_count = h_l.count() # total count of all data points
    
    pos_count = (h_l > 0).sum() # positive data points
    neg_count = (h_l < 0).sum() # negative data points
    
    pos_perc = (pos_count / total_count) *100 # % Of positive Days
    neg_perc = (neg_count / total_count) *100 # % Of negative Days 
    
    daily_pos_mean = data.loc[data['h_l']> 0, 'h_l'].mean() # Average of only Positive Return 
    daily_neg_mean = data.loc[data['h_l']< 0, 'h_l'].mean() # Average of only Negative Returns 
    
    pos_adj_freq = daily_pos_mean * pos_perc # Adjusted Daily positive Return
    neg_adj_freq = daily_neg_mean * neg_perc # Adjusted Daily negative Return
    
    # Standard Deviation Calculations for Close Returns for each Bound
    upper1 = avg_ret + 1 * std
    lower1 = avg_ret - 1 * std
    count_1 = data[(data['h_l'] >= lower1) & (data['h_l'] <= upper1)].shape[0]
    prc_count_1 = count_1 / total_count

    upper2 = avg_ret + 2 * std
    lower2 = avg_ret - 2 * std
    count_2 = data[(data['h_l'] >= lower2) & (data['h_l'] <= upper2)].shape[0]
    prc_count_2 = count_2 / total_count

    upper3 = avg_ret + 3 * std
    lower3 = avg_ret - 3 * std
    count_3 = data[(data['h_l'] >= lower3) & (data['h_l'] <= upper3)].shape[0]
    prc_count_3 = count_3 / total_count
    
             # Close data table
    h_l_stats_data = [
            # Positive Label
        {"Label": "Positive",
            "Mean": f"{daily_pos_mean:.2%}",
            "Count": pos_count,
            "Frequency %": f"{pos_perc}%",
            "Adj Return": f"{pos_adj_freq:.2f}%"},
        
        # Negative Label
        {"Label": "Negative",
            "Mean": f"{0}",
            "Count": 0,
            "Frequency %": f"{0}%",
            "Adj Return": f"{0}%"},
        ]
    
    h_l_stats_columns = [
        {"name": "", "id": "Label"},
        {"name": "Mean", "id": "Mean"},
        {"name": "Count", "id": "Count"},
        {"name": "Frequency %", "id": "Frequency %"},
        {"name": "Adj Return", "id": "Adj Return"}
        ]
    
    # Table 2 data
    h_l_std_data = [
        # Positive Label
        {"Label": "Std_1", "Upper Bound": f"{upper1:.2%}", "Lower Bound": f"{lower1:.2%}","Count":f"{count_1}","Count %":f"{prc_count_1:.2%}"},
        {"Label": "Std_2", "Upper Bound": f"{upper2:.2%}", "Lower Bound": f"{lower2:.2%}","Count":f"{count_2}","Count %":f"{prc_count_2:.2%}"},
        {"Label": "Std_3", "Upper Bound": f"{upper3:.2%}", "Lower Bound": f"{lower3:.2%}","Count":f"{count_3}","Count %":f"{prc_count_3:.2%}"},
    ]

    h_l_std_columns = [
        {"name": "", "id": "Label"},
        {"name": "Upper Bound", "id": "Upper Bound"},
        {"name": "Lower Bound", "id": "Lower Bound"},
        {"name": "Count", "id": "Count"},
        {"name": "Count %", "id": "Count %"},
    ]

    return {
        "h_l": h_l,
        "h_l_stats_data": h_l_stats_data,
        "h_l_stats_columns": h_l_stats_columns,
        "h_l_std_data": h_l_std_data,
        "h_l_std_columns": h_l_std_columns
    }