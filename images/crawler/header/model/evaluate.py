import numpy as np
import matplotlib.pyplot as plt
import torch

from sklearn.metrics import mean_absolute_error as MAE
from sklearn.metrics import mean_squared_error as MSE
from sklearn.metrics import mean_absolute_percentage_error as MAPE
from sklearn.metrics import r2_score as R2

# def evaluate(y_true, y_pred):
#     mae = MAE(y_true, y_pred)
#     rmse = np.sqrt(MSE(y_true, y_pred))
#     mape = MAPE(y_true, y_pred)
#     r2 = R2(y_true, y_pred)
    
#     print(f'mae: {mae:.4f}, rmse: {rmse:.4f}, mape: {mape:.4f}, r2: {r2:.4f}')
    

def plot_result(
    y_true, y_pred, start1, start2, date, 
    title, figsize = (20, 8), dpi = 70, fontsize = 20
):
    x1 = date[start1: start1 + len(y_true)]
    x2 = date[start2: start2 + len(y_true)]
    
    plt.figure(figsize = figsize, dpi = dpi)
    plt.suptitle(title, fontsize = fontsize, ha = 'center')
    plt.plot(x1, y_true[start1: ], color='orange', linewidth=2, markersize=12)
    plt.plot(x2, y_pred, color='cornflowerblue', linewidth=2, markersize=12)
    plt.legend(['y_true', 'y_pred'])
    plt.show()
    
def regression_report(y_true, pred, col_lst, verbose = True):
    if (len(y_true.shape) > 1) and (y_true.shape[1] > 1):
        mae = MAE(y_true, pred, multioutput='raw_values')
        rmse = np.sqrt(MSE(y_true, pred, multioutput='raw_values'))
        mape = MAPE(y_true, pred, multioutput='raw_values')
        r2 = R2(y_true, pred, multioutput='raw_values')
        
        if verbose:
            for i in range(y_true.shape[1]):
                title = col_lst[i]
                plt.figure(figsize = (20, 3), dpi = 70)
                plt.suptitle(title, fontsize = 20, ha = 'center')
                plt.plot(y_true[:, i], color='orange', linewidth=2, markersize=12)
                plt.plot(pred[:, i], color='cornflowerblue', linewidth=2, markersize=12)
                plt.legend(['y_true', 'y_pred'])
                plt.show()
                print(f'mae: {mae[i]:.4f}, rmse: {rmse[i]:.4f}, mape: {mape[i]:.4f}, r2: {r2[i]:.4f}\n\n')
            
    else:
        y_true = y_true.reshape(-1)
        pred = pred.reshape(-1)
        
        mae = MAE(y_true, pred)
        rmse = np.sqrt(MSE(y_true, pred))
        mape = MAPE(y_true, pred)
        r2 = R2(y_true, pred)

        if verbose:
            plt.figure(figsize = (20, 3), dpi = 70)
            plt.suptitle(title, fontsize = 20, ha = 'center')
            plt.plot(y_true, color='orange', linewidth=2, markersize=12)
            plt.plot(pred, color='cornflowerblue', linewidth=2, markersize=12)
            plt.legend(['y_true', 'y_pred'])
            plt.show()
            print(f'mae: {mae:.4f}, rmse: {rmse:.4f}, mape: {mape:.4f}, r2: {r2:.4f}')
    
    return mae, rmse, mape, r2
    


def plot_loss(train_loss, val_loss, figsize = (16, 5), dpi = 70):
    plt.figure(figsize = figsize, dpi = dpi)
    
    plt.subplot(1, 2, 1)
    plt.plot(train_loss, color = 'blue')
    plt.title('train')
    
    plt.subplot(1, 2, 2)
    plt.plot(val_loss, color = 'orange')
    plt.title('val')
    
    plt.show()