# Author: Midrar Adham
import os
import numpy as np
import pandas as pd

class resampling():

    def __init__(self):
        
        # GridLAB-D-related Settings
        self.resampling_rate = 60 * 24              # Water draw event each minute for a day
        self.datetime_one_minute = '1T'             # datetime library resampling rate translation
        self.simulation_date = '2021-12-25'         # GridLAB-D Simulation date must match the wd profiles
        self.simulation_ending_time = '23:59:00'    # GridLAB-D simulation time must match the wd profiles
        self.simulation_starting_time = '00:00:00'  # GridLAB-D simulation time must match the wd profiles
        self.resampling_rate_threshold = '00:01:00' # Format is hh:mm:ss. Resamples the data for one minute.
        
        # Resampling attributes:
        self.sum_draw = 0
        self.elapsed_time = pd.Timedelta(0)
        self.new_data = {'timestamp':[], 'draw':[]}


        # files Path settings:
        self.wd_files = "../outputs/"
        self.output_files = "../outputs/psu_feeder_wd_profiles"

        # Writing to csv file settings:
        self.file_counter = 0

    def sum_draws(self, file_name):
        '''
        This function sums up the time difference between the end draw time and start draw time and the 
        water draw events. If the summation of the difference becomes one minute, then that's the draw for one minute.

        Once the draws are summed up, the df becomes smaller in size. So we take the starting times 
        that corresponds with the summed water draws for one minute.
        
        NOTE: For GridLAB-D, we only care about start times of the water draws.
        '''
        
        df = pd.read_csv(self.wd_files+file_name)

        # Takes the difference between the end draw time and start draw time
        df["timestamp"] = pd.to_timedelta(pd.to_datetime(df["end_time"]) - pd.to_datetime(df["start_time"]))
        
        # Create new df to append data to it.
        
        self.new_df = pd.DataFrame(self.new_data)

        for i, row in df.iterrows():
            self.elapsed_time += row['timestamp']
            self.sum_draw += row['draw']

            if self.elapsed_time >= pd.Timedelta(f'{self.resampling_rate_threshold}'):
                new_row = {'timestamp':pd.Timedelta(f'{self.resampling_rate_threshold}'), 'draw':self.sum_draw}
                new_row_df = pd.DataFrame([new_row])
                self.new_df = pd.concat([self.new_df, new_row_df], ignore_index=True)
                self.elapsed_time = self.elapsed_time - pd.Timedelta(f'{self.resampling_rate_threshold}')
                self.sum_draw = 0
        
        self.new_df['timestamp'] = df['start_time']

    def create_full_day_df(self):

        self.new_df['timestamp'] = pd.to_datetime(self.new_df['timestamp']).dt.floor('min')
        self.new_df['timestamp'] = pd.to_datetime(f'{self.simulation_date}' + self.new_df['timestamp'].dt.strftime(' %H:%M:%S'))
        data = {'timestamp':pd.date_range(start=f'{self.simulation_date} {self.simulation_starting_time}', end=f'{self.simulation_date} {self.simulation_ending_time}', freq=f'{self.datetime_one_minute}'),
                'draw':np.zeros(self.resampling_rate)}
        
        full_day_df = pd.DataFrame(data)
        self.merged_dfs = pd.merge(full_day_df, self.new_df, on='timestamp', how='left')
        self.merged_dfs['draw_x'] = self.merged_dfs['draw_x'].fillna(self.merged_dfs['draw_y'])
        self.merged_dfs = self.merged_dfs.drop('draw_x', axis=1)
        self.merged_dfs = self.merged_dfs.rename(columns={'draw_y':'draw'})
        self.merged_dfs['draw'] = (self.merged_dfs['draw'].fillna(0)).round(6)

    def wr_csv(self, files):
        
        bedroom_num = ['1br','2br','3br','4br','5br']
        files_index = files.split('dwh-')[1]
        
        for br in bedroom_num:
            if br in files:
                output_file_names = f'{br}_{files_index}'
        
        self.merged_dfs.to_csv(f'{self.output_files}/wd_{output_file_names}', index = False, header=False)

if __name__ == '__main__':
    resample_data = resampling()
    
    for files in os.listdir(resample_data.wd_files):
        if files.startswith('std'):
            resample_data.sum_draws(files)
            resample_data.create_full_day_df()
            resample_data.wr_csv(files)