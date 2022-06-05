import glob
import json
import numpy as np
import pandas as pd
from datetime import datetime

def feature_generation(
    df_in: pd.DataFrame,
    cols: list,
    lags: list = [5, 20, 40, 60]
):
    df = df_in.copy()
    for col in cols:
        for lag in lags:
            roll = df[col].rolling(lag)
            df[f'{col}_mean_{lag}'] = roll.mean()
            df[f'{col}_std_{lag}'] = roll.std()
            df[f'{col}_median_{lag}'] = roll.median()
            df[f'{col}_max_{lag}'] = roll.max()
            df[f'{col}_min_{lag}'] = roll.min()

    df = df.iloc[max(lags): ].reset_index(drop = True)

    return df

def predict(
    model,
    preprocessing,
    data: pd.DataFrame,
    col_lst: list = ['tsmc', 'asml', 'amat', 'sumco'],
    start: str = '2022-05-29',
    end: str = '2022-12-31',
    date_format: str = '%Y-%m-%d',
    date_col:str = 'date',
    verbose: bool = True
):
    datelist = pd.date_range(start = start, end = end)
    start = datetime.strptime(start, date_format)
    end = datetime.strptime(end, date_format)
    distance = (end - start).days + 1

    col = len(col_lst)
    total_pred = np.zeros((distance, col))

    pred = np.zeros((1, col))
    for i, date in enumerate(datelist):
        if verbose:
            print(date.strftime(date_format))
        x = preprocessing(data[col_lst], col_lst).to_numpy()
        
        pred = np.asarray(np.round(model.predict(x)), dtype = 'int')

        #for j, model in enumerate(model_lst):
            #print(model.predict(x))
            #pred[0, j] = model.predict(x)[0]

        total_pred[i] = pred
        tmp = pd.DataFrame(pred, columns = col_lst)
        tmp[date_col] = date
        data = pd.concat([data, tmp], axis = 0).reset_index(drop = True)
        data = data.iloc[1: ]

    total_pred = pd.DataFrame(total_pred, columns = col_lst)
    total_pred[date_col] = datelist
    total_pred = total_pred.reindex(columns = [date_col] + col_lst)
    total_pred[col_lst] = total_pred[col_lst].astype(dtype = 'int')

    return total_pred

def get_csv_from_json(
    json_dir: str = './data/crawler_data',
    save_dir = None
):
    json_lst = glob.glob(f'{json_dir}/*.json')

    df = pd.DataFrame()
    json_dict = {
        'date': [],
        'TSMC': [],
        'ASML': [],
        'AM': [],
        'SUMCO': []
    }

    for json_path in json_lst:
        date = json_path.split('/')[-1].split('.')[0]
        date = datetime.strptime(date,"%Y-%m-%d")
        json_dict['date'].append(date)

        with open(json_path, newline='') as jsonfile:
            data = json.load(jsonfile)

        for key in data.keys():
            json_dict[key].append(data[key])

    for key in json_dict:
        df[key] = json_dict[key]

    df = df.sort_values(by = ['date']).reset_index(drop = True)
    
    if save_dir is not None:
        df.to_csv(f'{save_dir}/VolumneForFourCompany.csv', index = False)
    
    return df
