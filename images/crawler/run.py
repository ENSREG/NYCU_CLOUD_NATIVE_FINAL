import numpy as np
import pandas as pd
from joblib import load

from datetime import datetime, timedelta
from sklearn.linear_model import BayesianRidge
from sklearn.multioutput import MultiOutputRegressor

from header.model import feature_generation, predict
from header.crawler import get_today

if __name__ == '__main__':
    # -------- prepare data --------
    tmp = get_today()

    today = pd.DataFrame()
    for key in tmp.keys():
        today[key] = [tmp[key]]

    total = pd.read_csv('./data/GroundTruth.csv')
    total = pd.concat([total, today], axis = 0).reset_index(drop = True)
    df = total[total.shape[0] - 61: ]

    date_format = "%Y-%m-%d"
    start_date = (datetime.strptime(tmp['date'], date_format) + timedelta(days = 1)).strftime(date_format)

    col_name = ['TSMC', 'ASML', 'AM', 'SUMCO']

    # -------- predict --------
    # load model
    model = load('./ckpt/BayesianRidge.pkl')
    pred = predict(
        model,
        feature_generation,
        df,
        col_lst = col_name,
        start = start_date,
        end = '2022-12-31',
        verbose = False
    )

    # -------- save csv --------
    pred.to_csv('./data/Pred.csv', index = False)
    total.to_csv('./data/GroundTruth.csv', index = False)