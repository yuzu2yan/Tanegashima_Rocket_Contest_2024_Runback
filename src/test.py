import yaml
with open('settings.yaml') as yml:
    settings = yaml.safe_load(yml)
    
print(settings['destination']['latitude'])
print(settings['destination']['longitude'])