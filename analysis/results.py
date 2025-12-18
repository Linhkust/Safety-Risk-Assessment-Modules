import pandas as pd
import os
import ast

'''
basic information of panel members
'''
def response_combine(file_path='./simulation'):
    df = pd.DataFrame()
    for i, response in enumerate(os.listdir(file_path)):
        df = pd.concat([df, pd.read_csv(file_path + '/' + response)], ignore_index=True)
    return df

def pm_info():
    df = response_combine()
    df.iloc[:, :3].to_csv('./paper/pm_info.csv', index=False)

'''
Weights of probability, severity, exposure, detectability
'''
def weights1():
    df = response_combine()
    df['weights'] = df['Parameters_w'].apply(lambda x: eval(x))
    for index, column in enumerate(['probability', 'severity', 'exposure', 'detectability']):
        df[column] = df['weights'].apply(lambda x: round(x[index], 4))
    df.iloc[:, -4:].to_csv('./paper/weights_psed.csv', index=False)

'''
Weights of severity
'''
def weights2():
    df = response_combine()
    df['weights'] = df['Severity_w'].apply(lambda x: eval(x))
    for index, column in enumerate(['Number of total injuries',
                                    'Number of total fatalities',
                                    'Average injury rate',
                                    'Average fatality rate']):
        df[column] = df['weights'].apply(lambda x: round(x[index], 4))
    df.iloc[:, -4:].to_csv('./paper/weights_s.csv', index=False)

# subjective evaluation of frequency and detectability
def fd_eval():
    df = response_combine()
    df['f_eval'] = df['Exposure_e'].apply(lambda x: eval(x))



if __name__ == "__main__":
    fd_eval()