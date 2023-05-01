# Author: Midrar Adham

import os
import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

class resampling():

    def __init__(self):
        
        # GridLAB-D-related Settings
        self.resampling_rate = 60 * 24              # Water draw event each minute for a day
        self.datetime_one_minute = '1T'             # datetime library resampling rate translation
        self.simulation_date = '2021-12-25'         # GridLAB-D Simulation date must match the wd profiles
        self.simulation_ending_time = '23:59:00'    # GridLAB-D simulation time must match the wd profiles
        self.simulation_starting_time = '00:00:00'  # GridLAB-D simulation time must match the wd profiles
        self.resampling_rate_threshold = '00:01:00' # Format is hh:mm:ss. Resamples the data for one minute.

        # files Path settings:
        self.wd_files = "../outputs/"
        self.output_files = "../outputs/psu_feeder_wd_profiles/"
    
    def convert_to_unix(self, df):
        df['Time'] = pd.to_datetime(df['Time'])
        df.loc[:, 'Time'] = pd.to_datetime(df['Time'].dt.strftime('2021-12-25 %H:%M:%S'))
        df['Time_2'] = df['Time'].astype(int) // 10**9
        return df

    def adjust_ts_to_duration(self, df):
        df['Time_2'] = df['Time_2'] + df['Duration']
        df['timestamp'] = pd.to_datetime(df['Time_2'], unit='s')
        return df

    
    def concat_times(self, df):
        df['timestamp'] = pd.concat([df['Time'], df['timestamp']], axis=0).reset_index(drop=True)
        return df
    
    def sum_up_ts(self,df):
        resampled_df = pd.DataFrame(columns=['timestamp','gpm'])
        for index, row in df.iterrows():
            end_time = row['timestamp'] + pd.Timedelta(seconds=row['Duration'])
            temp_df = pd.DataFrame(pd.date_range(start=row['timestamp'], end=end_time, freq='min'), columns=['timestamp'])
            temp_df['gpm'] = row['Hot']
            resampled_df = pd.concat([resampled_df, temp_df], ignore_index=True)
        return resampled_df
    
    def floor_minutes(self, df):
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.floor('min')
        return df
    
    def new_data(self,df):
        new_index = pd.date_range(start='2021-12-25 00:00:00', end='2021-12-25 23:59:00', freq='1min')
        data = {'timestamp':pd.date_range(start='2021-12-25 00:00:00',
        end='2021-12-25 23:59:00', freq='1min'),'gpm':np.zeros(60*24)}
        df = pd.DataFrame(data)
        return df
    
    def merge_data(self, df, new_df):
        new_df['timestamp'] = pd.to_datetime(new_df['timestamp'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        merged_df = pd.merge(new_df,df, on='timestamp', how='left')
        merged_df['gpm'] = merged_df['gpm_y'].fillna(merged_df['gpm_x'])
        merged_df = merged_df.drop(['gpm_x','gpm_y'], axis=1)
        return merged_df

    def write_files (self, df, f_name):
        df.to_csv(f'{self.output_files}{f_name}', index=False)
    
    def set_output_f_name(self,file):
        br = file.split('.')[0]
        br = file.replace("std","wd").replace("-dwh-","-")
        return br


if __name__ == '__main__':
    resample_data = resampling()
    rooms = ['std-1br','std-2br','std-3br','std-4br','std-5br']
    for br in rooms:
        for files in os.listdir(resample_data.wd_files):
            if files.startswith('std') and br in files:
                df = pd.read_csv(resample_data.wd_files+files)
                df = resample_data.convert_to_unix(df)
                df = resample_data.adjust_ts_to_duration(df)
                df = resample_data.concat_times(df)
                df = resample_data.sum_up_ts(df)
                df = resample_data.floor_minutes(df)
                new_df = resample_data.new_data(df)
                df = resample_data.merge_data(df, new_df)
                f_name = resample_data.set_output_f_name(files)
                resample_data.write_files(df,f_name)
                