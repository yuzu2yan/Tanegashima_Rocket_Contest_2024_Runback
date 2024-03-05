import yaml
import sys
# sys.path.append('./image processing')

from image_processing import cone_detection

with open('settings.yaml') as yml:
    settings = yaml.safe_load(yml)

    
# print(settings['destination']['latitude'])
# print(settings['destination']['longitude'])