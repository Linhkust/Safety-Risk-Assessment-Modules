'Fuzzy inference system for SCEA'
'''
Karasan, A., Ilbahar, E., Cebi, S., & Kahraman, C. (2018). 
A new risk assessment approach: Safety and Critical Effect Analysis (SCEA) and its extension with Pythagorean fuzzy sets. 
Safety science, 108, 173-187.
'''
import pandas as pd

def f_scea(p, s, e, d):
    data = pd.read_csv('fuzzy_scea.csv', header=None)
    scale = [1, 3, 5, 7, 9]

    column_row = []
    for i in range(5):
        column_row.append([j + 5 * i for j in range(5)])
    # p, d
    # s, e
    p_index = scale.index(p)
    s_index = scale.index(s)
    e_index = scale.index(e)
    d_index = scale.index(d)
    column_index = column_row[d_index][p_index]
    row_index = column_row[e_index][s_index]
    return data.iloc[column_index, row_index]