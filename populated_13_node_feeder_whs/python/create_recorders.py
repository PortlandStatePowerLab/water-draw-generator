import os
import re
import glm
import json
import subprocess
from pprint import pprint as pp


class create_glm_objects():

    def __init__(self):
        # We have from one to five bedrooms water draw profiles, modify as needed:
        self.room_num = ['1br','2br','3br','4br','5br']

        # Paths:
        self.glm_path = '../glm/'                                               # glm output file destination
        self.json_path = '../json/'                                             # json files destination
        self.downstream_obj = 'downstream_objects'                              # GridLAB-D file name
        self.up_stream_objects = '13_node_feder_whs'                            # GridLAB-D file name
        self.water_draw_profiles = '../../outputs/psu_feeder_wd_profiles/'      # Grabs the water draw profiles
        
        # object multi recorder properties:
        self.recorder_time_resolution = 60
        self.property = "measured_real_power"
        
        # open glm files
        self.recorders_file_name = 'multi_recorders.glm'
        self.player_objects_file_name = 'player_objects.glm'

        # Change the following to True if glm2json (or viceversa ) is needed 
        self.glm_json = {
            'False':'json2glm(self)',
            'False':'glm2json(self)'
        }

    def conversions(self):
        for key, value in self.glm_json.items():
            if key == 'True':
                eval(f"create_glm_objects.{value}")

    # glm to json and vice-versa:
    def json2glm(self):
        p1 = subprocess.Popen(f'json2glm -p {self.json_path}{self.downstream_obj}.json > {self.glm_path}{self.downstream_obj}.glm')
        p1.wait()

    def glm2json(self):
        p1 = subprocess.Popen(f'glm2json -p {self.glm_path}{self.downstream_obj}.glm > {self.glm_path}{self.downstream_obj}.json')
        p1.wait()

    # Open recorder and player files
    def open_files(self):
        self.down_stream_obj = glm.load(f'{self.glm_path}{self.downstream_obj}.glm')
        self.water_heaters = open (f'{self.glm_path}waterheaters.glm', 'w')
        self.multi_recorders = open (f'{self.glm_path}{self.recorders_file_name}','w')
        self.player_objects = open (f'{self.glm_path}{self.player_objects_file_name}', 'w')
        

    
    # Pull meter object names to link to recorders
    def setup_recorder_names(self):
        
        self.node = []
        self.meter_names = []
        self.recorders_property = []

        for i in self.down_stream_obj['objects']:
            if i['name'] == 'triplex_meter':                    
                self.meter_names.append(i['attributes']['name'])
            if i['name'] == 'waterheater':
                self.node.append(re.findall(r'\d+',i['attributes']['name'])[0])
                    
    # Get properties for multi-recorder objects
    def setup_recorder_properties(self):
        
        power_prop = [str(self.property) for i in range(960)]
        for names, pwr_prop in zip(self.meter_names, power_prop):
            rec = f'{names}:{pwr_prop}'
            self.recorders_property.append(rec)
        
        return self.recorders_property

    '''
    shuffle water profiles function gets an equal number of each br water draw profile. If the user
    wants to get only the 1br category, then the number of DERs in the feeder is divided by the 
    length of the br list.
    '''
    def shuffle_wd_files(self,room_num, wd_profile_per_category):
        
        self.wd_profiles = []
        for file_name in os.listdir(self.water_draw_profiles):
            num_profiles = 0
            for br in room_num:
                if br in file_name and num_profiles < wd_profile_per_category:
                    self.wd_profiles.append(file_name)
                    num_profiles += 1
            if len(self.wd_profiles) > 960:
                break

    '''
    print multi-recorder objects to glm file.
    NOTE: GridLAB-D does not read more than 25 meter objects in one multi-recorder object. This number 
    could be different from one OS to another. 
    '''

    def print_multi_recorders(self):
        
        counter = 1
        for i in range(0, len(self.recorders_property), 25):
            group = self.recorders_property[i: i+25]
            print(f"object multi_recorder {{\n\tinterval {self.recorder_time_resolution};\n\tproperty {','.join(str(meters) for meters in group)};\n\tfile ./{self.glm_path}glm_output/meter_{counter}.csv;\n}}", file=self.multi_recorders)
            counter +=1
        self.multi_recorders.close()
    
    def print_player_objects(self):
        for node, wd_file in zip(self.node, self.wd_profiles):
            wd_file = wd_file.split('.csv')[0]
            print(f'object player {{\n\tname wd_{node}_{wd_file};\n\tfile "{self.water_draw_profiles}{wd_file}.csv";\n}};',file=self.player_objects)
        
        self.player_objects.close()
        
    def adjust_wh_objects_properties(self):
        data = glm.load('../glm/downstream_objects.glm')
        counter = 0

        for obj in data['objects']:
            
            if obj['name'] == 'waterheater':
                wd_file = self.wd_profiles[counter].split('.csv')[0]
                obj['attributes']['water_demand'] = wd_file
                print(f"object waterheater {{\n", file=self.water_heaters)
                print(f"\tname {obj['attributes']['name']};", file=self.water_heaters)
                print(f"\tparent {obj['attributes']['parent']};", file=self.water_heaters)
                print(f"\tlocation {obj['attributes']['location']};", file=self.water_heaters)
                print(f"\ttemperature {obj['attributes']['temperature']};", file=self.water_heaters)
                print(f"\twater_demand wd_{self.node[counter]}_{obj['attributes']['water_demand']}.value;",
                      file=self.water_heaters)
                print(f"\theat_mode {obj['attributes']['heat_mode']};", file=self.water_heaters)
                print(f"\theating_element_capacity {obj['attributes']['heating_element_capacity']};",
                      file=self.water_heaters)
                print(f"\tthermostat_deadband {obj['attributes']['thermostat_deadband']};", file=self.water_heaters)
                print(f"\ttank_setpoint {obj['attributes']['tank_setpoint']};", file=self.water_heaters)
                print(f"\ttank_UA {obj['attributes']['tank_UA']};", file=self.water_heaters)
                print(f"\ttank_volume {obj['attributes']['tank_volume']};", file=self.water_heaters)
                print("\n};", file=self.water_heaters)
                counter +=1
        self.water_heaters.close()
        

if __name__== '__main__':
    glm_objects = create_glm_objects()
    glm_objects.conversions()
    glm_objects.open_files()
    glm_objects.setup_recorder_names()
    glm_objects.setup_recorder_properties()
    wd_profile_per_category = int(960/len(glm_objects.room_num))
    glm_objects.shuffle_wd_files(glm_objects.room_num, wd_profile_per_category)
    glm_objects.print_multi_recorders()
    glm_objects.print_player_objects()
    glm_objects.adjust_wh_objects_properties()