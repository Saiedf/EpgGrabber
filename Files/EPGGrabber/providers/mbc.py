#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

try:
    from .__init__ import *
except:
    from __init__ import *

import requests
import io
import threading
import sys
import os
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
import time
from time import sleep, strftime
import json

if sys.version_info[0] < 3:
    import codecs
    open = codecs.open

time_zone = tz()

head = {
    "Content-Type": "application/json; charset=utf-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://api3.shahid.net/"
}

channels_code = sorted([
    "387248-MBC1", "400917-MBC2", "409385-MBC3", "400919-MBC4", "387937-MBC5", "409387-MBC Bollywood",
    "387251-MBC Drama", "387294-MBC Iraq", "418308-MBC Persia", "387290-MBC Masr", "387293-MBC Masr 2",
    "400924-MBC Max", "387296-MBC Plus Drama", "388567-MBC FM", "946948-Al Ekhbaria", "387286-Al Arabiya",
    "1003218-Al Arabiya Business", "387288-Alhadath",  "955107-SSC News", "862837-Alsharq", "997605-Alsharq Documentary",
    "1001845-Alsharq Discovery", "946946-Saudi ch for Quran", "946942-Saudi ch for Sunnah", "992538-Al La'bah", 
    "946938-Al saudia", "999927-Al Saudia Alaan TV", "946945-Thikrayatt","946940-SBC", "414449-Wanasah", "409390-Spacetoon", 
    "1037534-Arabs Got Talent","975435-Bab Al Hara","983124-Masrah Misr", "49922754576681-Bidaya",
    "951783-BIG TIME", "49922904934759-Big Time Plus", "1039070-Comedy Khaleeji", "1029746-Khozami Radio", "388566-Panorama FM", 
    "986064-Movies Action", "986069-Movies Thriller", "999399-Nature Time", "49922661692898-Red Bull TV", "963330-Top Chef", 
    "988045-Maraaya", "986014-Abdul Majeed Abdullah", "986346-Mohammad Abdu", "986024-Rashid Al Majid", "49922763891977-Majid Al Mohandes", "49922763510387-Tarab", "969745-Nasser Al Qassabi", 
    "1005232-Selfie", "989622-Shahid Aflam", "963543-Tash", "977946-Al Assouf" ])

lock = threading.Semaphore(2)

def xml_header(path, channels):
    file = open(path, 'w')
    if sys.version_info[0] >= 3:
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        file.write('<tv generator-info-name="By ZR1">')
    else:
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n'.decode('utf-8'))
        file.write(('<tv generator-info-name="By ZR1">').decode('utf-8'))
    file.close()

    for channel in channels:
        # Remove the word "channel" from the display name
        display_name = channel.replace(" Channel", "").replace(" channel", "")
        
        with io.open(path, "a", encoding='UTF-8') as f:
            if sys.version_info[0] >= 3:
                f.write("\n" + '  <channel id="' + channel + '">' + '<display-name lang="en">' + display_name + '</display-name>' +' </channel>\r')
            else:
                f.write(("\n" + '  <channel id="' + channel + '">' + '<display-name lang="en">' + display_name + '</display-name>' +' </channel>\r').decode('utf-8'))

def close_xml(path):
    file = open(path, 'a')
    if sys.version_info[0] >= 3:
        file.write('\n' + '</tv>')
    else:
        file.write(('\n' + '</tv>').decode('utf-8'))

    file.close()

def mbc_epg(code):
    try:
        channel_id, channel_name = code.split('-', 1)
        # Remove the word "channel" from the channel name
        channel_name = channel_name.replace(" Channel", "").replace(" channel", "")
        
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        from_date = today.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'  # من اليوم
        to_date = (today + timedelta(days=6)).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'  # إلى اليوم + 6 أيام

        # Print the channel name as it starts loading
        #print("Loading {}...".format(channel_name))
        #sys.stdout.flush()

        with requests.Session() as s:
            s.mount('https://', HTTPAdapter(max_retries=10))
            retries = 3
            for attempt in range(retries):
                try:
                    url = s.get(
                        'https://api3.shahid.net/proxy/v2.1/shahid-epg-api/?language=ar&from={0}&to={1}&csvChannelIds={2}&country=EG'.format(from_date, to_date, channel_id),
                        headers=head
                    )
                    if url.status_code == 200:
                        break
                    else:
                        print("Attempt {} failed for {}. Status code: {}".format(attempt + 1, channel_name, url.status_code))
                        sys.stdout.flush()
                        time.sleep(5)
                except Exception as e:
                    print("Error fetching data for {}: {}".format(channel_name, e))
                    sys.stdout.flush()
                    time.sleep(5)
            if url.status_code != 200:
                print("Failed to fetch data for {}. Status code: {}".format(channel_name, url.status_code))
                sys.stdout.flush()
                return
            try:
                data = url.json()
            except ValueError as e:
                print("Invalid JSON response for {}: {}".format(channel_name, e))
                sys.stdout.flush()
                return
            if data and isinstance(data, dict) and 'items' in data:
                for channel in data['items']:
                    if channel['channelId'] == channel_id and 'items' in channel:
                        for program in channel['items']:
                            title = program.get('title', 'No Title') or 'No Title'
                            start_time = program.get('from', '') or ''          
                            end_time = program.get('to', '') or ''            
                            description = program.get('description', 'No Description') or 'No Description' 
                            title = title.strip()
                            start_time = start_time.strip()
                            end_time = end_time.strip()
                            description = description.strip()

                            # Initialize variables to avoid referencing before assignment
                            start = end = None

                            try:
                                # Handle both 'Z' and '+00:00' timezone formats
                                start_time_clean = start_time.replace('Z', '').split('+')[0]
                                end_time_clean = end_time.replace('Z', '').split('+')[0]

                                # Parse the datetime without timezone
                                start = datetime.strptime(start_time_clean, '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y%m%d%H%M%S')
                                end = datetime.strptime(end_time_clean, '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y%m%d%H%M%S')
                            except Exception as e:
                                print("Error parsing date for {}: {}".format(channel_name, e))
                                sys.stdout.flush()
                                continue

                            if start and end:  # Only write if both start and end are valid
                                ch = 2 * ' ' + '<programme start="' + str(start) + ' ' + time_zone + '" stop="' + str(end) + ' ' + time_zone + '" channel="' + channel_name + '">\n'
                                ch += 4 * ' ' + '<title lang="ar">' + (title if title else 'No Title').replace('&', 'and') + '</title>\n'
                                ch += 4 * ' ' + '<desc lang="ar">' + (description if description else 'No Description').replace('&', 'and') + '</desc>\n  </programme>\r'
                                with io.open(EPG_ROOT + '/mbc.xml', "a", encoding='UTF-8') as f:
                                    f.write(ch)
                        if end:  # Only print if end is valid
                            print("{} epg ends at : {}".format(channel_name, datetime.strptime(end, '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M')))
                            sys.stdout.flush()
                    else:
                        print("No items found for {}".format(channel_name))
                        sys.stdout.flush()
            else:
                print("No valid data found for {}".format(channel_name))
                sys.stdout.flush()
    except Exception as e:
        print("Error in mbc_epg function for {}: {}".format(code, e))
        sys.stdout.flush()
    finally:
        lock.release()

def main():
    print('**************MBC_EPG******************')
    print("Downloading MBC_EPG Guide Please wait....")
    sys.stdout.flush()
    import json
    with open(PROVIDERS_ROOT, 'r') as f:
        data = json.load(f)
    for channel in data['bouquets']:
        if channel["bouquet"] == "mbc":
            channel['date'] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
    with open(PROVIDERS_ROOT, 'w') as f:
        json.dump(data, f)

    channels = [ch.split('-')[1] for ch in channels_code]

    xml_header(EPG_ROOT + '/mbc.xml', channels)

    thread_pool = []
    for code in channels_code:
        thread = threading.Thread(target=mbc_epg, args=(code,))
        thread_pool.append(thread)
        thread.start()
        sleep(1)
        lock.acquire()
    for thread in thread_pool:
        thread.join()
    close_xml(EPG_ROOT + '/mbc.xml')

    if os.path.exists('/var/lib/dpkg/status'):
        print('Dream os image found\nSorting data please wait.....')
        sys.stdout.flush()
        import xml.etree.ElementTree as ET
        tree = ET.parse(EPG_ROOT + '/mbc.xml')
        data = tree.getroot()
        els = data.findall("*[@channel]")
        new_els = sorted(els, key=lambda el: (el.tag, el.attrib['channel']))
        data[:] = new_els
        tree.write(EPG_ROOT + '/mbc.xml', xml_declaration=True, encoding='utf-8')

    print('**************FINISHED******************')
    sys.stdout.flush()

if __name__ == '__main__':
    main()