import numpy as np
import pandas as pd
import os
import plotly.express as px
import ast
from pyrepo_mcda import normalizations
from jenkspy import JenksNaturalBreaks
from fuzzy_scea import f_scea
import zipfile

'''demographic information'''
# 解压缩
def un_zip(file_name):
    f = zipfile.ZipFile(file_name, 'r')
    new_path = os.path.join(os.path.dirname(file_name), 'response')

    os.mkdir(new_path)
    for file in f.namelist():
        f.extract(file, str(new_path))  # 解压位置
    f.close()

    df = pd.DataFrame()
    for i, response in enumerate(os.listdir(new_path)):
        response_file_path = os.path.join(new_path, response)
        df = pd.concat([df, pd.read_csv(response_file_path)], ignore_index=True)
    return df

def response_combine(file_path):
    df = pd.DataFrame()
    for i, response in enumerate(os.listdir(file_path)):
        df = pd.concat([df, pd.read_csv(file_path + '/' + response)], ignore_index=True)
    return df

def demographic(df):
    roles = df['Role'].value_counts().reset_index()
    years = df['Years of experience'].value_counts().reset_index()
    education = df['Education level'].value_counts().reset_index()
    return roles, years, education

def demographic_pie(df, i):
    fig = px.pie(data_frame=demographic(df)[i], values='count', names=df.columns[i], hole=.3)
    return fig

'''
Average weights of parameters and severity criteria
'''
def average_weight(df, column):
    init = []
    for i in range(len(df)):
        p_w = ast.literal_eval(df.loc[i, column])
        init.append(p_w)

    init = np.array(init)
    return np.mean(init, axis=0)

''''
Normalized criteria evaluation results of probability, severity, exposure and detectability
'''
def min_max_normalize(df, types=1):
    df = normalizations.minmax_normalization(matrix=df, types=types)
    return df

def probability_index(e):
    normalized_e = np.array(e.iloc[:, 2]).reshape(len(e), 1)
    return min_max_normalize(df=normalized_e).flatten()

def severity_e(e):
    normalized_s =np.array(e.iloc[:, 3:]).reshape(len(e), len(e.iloc[:, 3:].columns))
    return min_max_normalize(df=normalized_s)

def severity_index(df, e):
    severity_w = average_weight(df=df, column='Severity_w')
    severity_eval = severity_e(e=e)
    return min_max_normalize(df=np.sum(severity_eval * severity_w, axis=1).reshape(len(e), 1)).flatten()

def severity_table(df, e):
    severity_values = pd.DataFrame(np.around(severity_index(df, e), 3), columns=['Severity Index'])
    return pd.concat([e.iloc[:, :2], severity_values], axis=1)

def exposure_detectability(df, column):
    init = []
    for i in range(len(df)):
        e_d = [int(x) for x in ast.literal_eval(df.loc[i, column])]
        init.append(e_d)

    init = np.array(init)
    return np.mean(init, axis=0)

def exposure_detectability_index(df, column):
    _eval = exposure_detectability(df=df, column=column)
    return min_max_normalize(df=np.array(_eval).reshape(len(_eval), 1)).flatten()

''''
SCEA categories of probability, severity, exposure and detectability
'''
def p_category(e):
    p = probability_index(e=e)
    jnb = JenksNaturalBreaks(5)
    jnb.fit(p)
    return 2 * jnb.labels_ + 1

def s_category(df, e):
    s = severity_index(df=df, e=e)
    jnb = JenksNaturalBreaks(5)
    jnb.fit(s)
    return 2 * jnb.labels_ + 1

def e_category(df):
    e = exposure_detectability_index(df=df, column='Exposure_e')
    jnb = JenksNaturalBreaks(5)
    jnb.fit(e)
    return 2 * jnb.labels_ + 1

def d_category(df):
    d = exposure_detectability_index(df=df, column='Detectability_e')
    jnb = JenksNaturalBreaks(5)
    jnb.fit(d)
    return 2 * jnb.labels_ + 1

def risk_magnitude(df, eval):
    p = p_category(eval)
    s = s_category(df, eval)
    e = e_category(df)
    d = d_category(df)
    w = average_weight(df, 'Parameters_w')
    rm_values = []
    for i in range(len(eval)):
        risk_category = [p[i], s[i], e[i], d[i]]
        rm_value = np.prod(np.power(risk_category, w))
        rm_values.append(rm_value)

    # Our Study: Negligible, Minor, Major, Critical
    jnb = JenksNaturalBreaks(4)
    jnb.fit(rm_values)

    # Fuzzy_SCEA: Negligible, Minor, Major, Critical
    rm_category = []
    for i in range(len(eval)):
        rm_category.append(f_scea(p=p[i],
                                  s=s[i],
                                  e=e[i],
                                  d=d[i]))

    return rm_values, jnb.labels_, rm_category

def rm_table(df, eval):
    rm_scales = ['Ng', 'Mn', 'Mj', 'Cr']

    p = p_category(eval)
    s = s_category(df, eval)
    e = e_category(df)
    d = d_category(df)

    table = pd.DataFrame({
    'Probability': p,
    'Severity': s,
    'Exposure': e,
    'Detectability': d,
     'RM values': np.around(risk_magnitude(df, eval)[0], 3),
     'RM category': [rm_scales[i] for i in risk_magnitude(df, eval)[1]],
     'Fuzzy SCEA': risk_magnitude(df, eval)[2]
                        })
    return pd.concat([eval.iloc[:, :2], table], axis=1)

