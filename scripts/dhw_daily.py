import os
import pandas as pd

class extract_files():

    def __init__(self):

        self.path = '../data/'
        self.output = '../outputs/'
    
    def read_files (self, file):
        return pd.read_csv(self.path+file)
    
    def format_timestamp (self, df): # Not in main
        
        df['Time'] =  pd.to_datetime(df['Time'], format='%m/%d %I:%M:%S %p')
        df['Time'] = df['Time'].dt.strftime('%d-%m-%Y %H:%M:%S')
        df['Time'] = pd.to_datetime(df['Time'], format='%d-%m-%Y %H:%M:%S')
        return df
    
    def adjust_date (self, df): # Not in main
        df['Time'] = pd.to_datetime(df['Time'])
        return df
    
    def extract_each_day(self,df):
        
        df = self.format_timestamp(df)
        df = self.adjust_date(df)
        groups = df.groupby(pd.Grouper(key='Time', freq='D'))
        
        return groups

    def set_output_file_names(self, files, counter):
        
        f_name = f"{files.split('.')[0]}-{counter}"
        return f_name

    def write_files(self, group, f_name):
        group.to_csv(f"{self.output}/{f_name}.csv", index=False)

if __name__ == '__main__':
    get_f = extract_files()
    rooms = ['std-1br','std-2br','std-3br','std-4br','5br']
    for file in os.listdir(get_f.path):
        if file.startswith('std'):
            df = get_f.read_files(file)
            df = get_f.format_timestamp(df)
            groups = get_f.extract_each_day(df)
            for br in rooms:
                counter = 1
                for name, group in groups:
                    f_name = get_f.set_output_file_names(file, counter)
                    get_f.write_files(group,f_name)
                    counter += 1