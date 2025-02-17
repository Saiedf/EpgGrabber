#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import io
import re
import sys
import json
import requests
from datetime import datetime, timedelta
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import fileinput

# Ignore insecure request warnings
warnings.filterwarnings('ignore', category=InsecureRequestWarning)

# Constants
try:
    from __init__ import EPG_ROOT, PROVIDERS_ROOT
except ImportError:
    from __init__ import EPG_ROOT, PROVIDERS_ROOT

# Paths
input_path = os.path.join(EPG_ROOT, 'saudiarabia4.xml')
output_path = os.path.join(EPG_ROOT, 'out.xml')

# List of changes to apply
List_Chang = [
    # Example: ('old_text', 'new_text'),
    # Add your specific changes here
]
def main():
    print("*****************Saudiarabia4_iet5 EPG******************")
    sys.stdout.flush()
    print("Downloading Saudiarabia1_iet5 EPG guide\nPlease wait....")
    sys.stdout.flush()
    try:
        # Download the XML file
        response = requests.get('https://www.open-epg.com/files/saudiarabia4.xml', verify=False)
        if response.status_code == 200:
            with io.open(input_path, 'w', encoding="utf-8") as f:
                f.write(response.text)
            print("##########################################")
            print("Saudiarabia4.xml Downloaded Successfully")
            print("##########################################")

            # Apply the transformations
            apply_changes()
            # Adjust times in the XML
            adjust_times()
            # Remove duplicate lines
            remove_duplicates()
            # Rename the file
            rename_file()
            # Update providers JSON
            update_providers()
            # Remove specific lines
            remove_specific_lines()
            print('**************FINISHED******************')
            sys.stdout.flush()
        else:
            print("Failed to download /saudiarabia4.xml. Status code: {}".format(response.status_code))
    except requests.exceptions.RequestException as e:
        print("Failed to download /saudiarabia4.xml: {}".format(e))

def apply_changes():
    for old_text, new_text in List_Chang:
        for line in fileinput.input(input_path, inplace=True):
            if old_text in line:
                line = line.replace(old_text, new_text)
            sys.stdout.write(line)

def adjust_times():
    with io.open(input_path, 'r', encoding="utf-8") as f:
        xml_data = f.read()

    def adjust_start_time(match):
        original_time = datetime.strptime(match.group(1), '%Y%m%d%H%M%S')
        adjusted_time = original_time + timedelta(hours=3)  # Changed to +3 hours
        return 'start="{} +0300"'.format(adjusted_time.strftime('%Y%m%d%H%M%S'))  # Updated to +0300

    def adjust_stop_time(match):
        original_time = datetime.strptime(match.group(1), '%Y%m%d%H%M%S')
        adjusted_time = original_time + timedelta(hours=3)  # Changed to +3 hours
        return 'stop="{} +0300"'.format(adjusted_time.strftime('%Y%m%d%H%M%S'))  # Updated to +0300
        print("The time is set to +0300 ,and if your time is different,")  # Updated to +0300

    # Adjust the start and stop times
    xml_data = re.sub(r'start="(\d{14}) \+0000"', adjust_start_time, xml_data)
    xml_data = re.sub(r'stop="(\d{14}) \+0000"', adjust_stop_time, xml_data)

    with io.open(input_path, 'w', encoding="utf-8") as f:
        f.write(xml_data)

def remove_duplicates():
    lines_seen = set()
    with open(output_path, 'w') as output_file:
        for line in open(input_path, 'r'):
            if line not in lines_seen:
                output_file.write(line)
                lines_seen.add(line)

def rename_file():
    os.remove(input_path)
    os.rename(output_path, input_path)
    print("saudiarabia4.xml file successfully created")
    print("############################################################")
    print("The time is set to +0300 ,and if your time is different,")  # Updated to +0300
    print("you can modify the saudiarabia4iet5.py file at the following path:")
    print("/usr/lib/enigma2/python/Plugins/Extensions/EPGGrabber/providers/")
    print("############################################################")

def update_providers():
    with open(PROVIDERS_ROOT, 'r') as f:
        data = json.load(f)
        for channel in data['bouquets']:
            if channel["bouquet"] == "saudiarabia4iet5":
                channel['date'] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
    with open(PROVIDERS_ROOT, 'w') as f:
        json.dump(data, f, indent=4)

# Remove lines containing specified data and empty lines
def remove_specific_lines():
    with open(input_path, 'r') as f:
        lines = f.readlines()
    with open(input_path, 'w') as f:
        for line in lines:
            if '<icon src="https://' not in line and '<url>https://' not in line and '<category' not in line and line.strip():
                f.write(line)

def change_data_list(old_text, new_text, file_path):
    for line in fileinput.input(file_path, inplace=True):
        if old_text in line:
            line = line.replace(old_text, new_text)
        sys.stdout.write(line)

def change(list_changes):
    for change_expr in list_changes:
        change_data_list(change_expr[0], change_expr[1], input_path)

if __name__ == "__main__":
    main()