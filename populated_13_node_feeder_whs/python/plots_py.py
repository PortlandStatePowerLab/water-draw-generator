import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.dates import MonthLocator, DateFormatter

glm_outpu_files_path = "../glm/glm_output/"

def clean_files (df):
    df['# timestamp'] = df['# timestamp'].apply(lambda x: x.rstrip('UTC'))
    return df

def plots(df, files):
    timestamp = pd.to_datetime(df['# timestamp'])
    for col in df.columns[1:]:
        file_names = (col.split('tn_meter_')[1]).split(':')[0]
        print(file_names)
        fig, ax = plt.subplots(1,figsize=(12,8))
        ax.xaxis.set_major_locator(ticker.MaxNLocator(25))
        ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
        ax.plot(timestamp, df[col])
        plt.xlabel('timestamp')
        plt.ylabel('Watts')
        plt.title(f'../../outputs/psu_feeder_wd_profiles/wd_{file_names}.csv')
        plt.xticks(rotation=45)
        plt.grid()
        plt.show()

def main(glm_outpu_files_path):

    for files in os.listdir(glm_outpu_files_path):
        
        df = pd.read_csv(glm_outpu_files_path+files, skiprows=range(0,7))
        df = clean_files(df)
        plots(df, files)
        

main(glm_outpu_files_path)