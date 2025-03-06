#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
try:
    from .__init__ import *
except:
    from __init__ import *
import requests
import re
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

BASE_URL = "https://api3.shahid.net/proxy/v2.1/editorial/carousel?request=%7B%22pageNumber%22:{},%22pageSize%22:100,%22id%22:%22Main%2FEGYPT%2Flivestream%2FEGY-Crm-live-channels%22%7D&country=EG"

def extract_channel_name(product_urls):
    for priority in ["/en/livestream/", "/livestream/"]:
        name = next((re.search(r"/livestream/([^/]+)/", url["url"]).group(1).replace("-", " ").title()
                     for url in product_urls if priority in url["url"]), None)
        if name:
            return name
    return None

def fetch_channels():
    channels_code = []
    for page in range(3):
        response = requests.get(BASE_URL.format(page))
        if response.status_code == 200:
            for item in response.json().get("editorialItems", []):
                channel_id = str(item["item"]["id"])
                channel_name = extract_channel_name(item["item"].get("productUrls", []))
                if channel_name:
                    # Fixed f-string to Python 2 format
                    channels_code.append((channel_name, "{0}-{1}".format(channel_id, channel_name)))
    
    return [code for _, code in sorted(channels_code)]

channels_code = fetch_channels()

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
        channel_name = channel_name.replace(" Channel", "").replace(" channel", "")
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        from_date = today.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        to_date = (today + timedelta(days=6)).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
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
                        print("Attempt {0} failed for {1}. Status code: {2}".format(attempt + 1, channel_name, url.status_code))
                        sys.stdout.flush()
                        time.sleep(5)
                except Exception as e:
                    print("Error fetching data for {0}: {1}".format(channel_name, e))
                    sys.stdout.flush()
                    time.sleep(5)
            if url.status_code != 200:
                print("Failed to fetch data for {0}. Status code: {1}".format(channel_name, url.status_code))
                sys.stdout.flush()
                return
            try:
                data = url.json()
            except ValueError as e:
                print("Invalid JSON response for {0}: {1}".format(channel_name, e))
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
                            try:
                                start_time_clean = start_time.replace('Z', '').split('+')[0]
                                end_time_clean = end_time.replace('Z', '').split('+')[0]

                                start_dt = datetime.strptime(start_time_clean, '%Y-%m-%dT%H:%M:%S.%f')
                                start_dt += timedelta(hours=2)
                                start = start_dt.strftime('%Y%m%d%H%M%S')

                                end_dt = datetime.strptime(end_time_clean, '%Y-%m-%dT%H:%M:%S.%f')
                                end_dt += timedelta(hours=2)
                                end = end_dt.strftime('%Y%m%d%H%M%S')
                            except Exception as e:
                                print("Error parsing date for {0}: {1}".format(channel_name, e))
                                sys.stdout.flush()
                                continue
                            if start and end:
                                ch = 2 * ' ' + '<programme start="' + str(start) + ' ' + time_zone + '" stop="' + str(end) + ' ' + time_zone + '" channel="' + channel_name + '">\n'
                                ch += 4 * ' ' + '<title lang="ar">' + (title if title else 'No Title').replace('&', 'and') + '</title>\n'
                                ch += 4 * ' ' + '<desc lang="ar">' + (description if description else 'No Description').replace('&', 'and') + '</desc>\n  </programme>\r'
                                with io.open(EPG_ROOT + '/mbc.xml', "a", encoding='UTF-8') as f:
                                    f.write(ch)
                        if end:
                            print("{0} epg ends at : {1}".format(channel_name, datetime.strptime(end, '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M')))
                            sys.stdout.flush()
                    else:
                        print("No items found for {0}".format(channel_name))
                        sys.stdout.flush()
            else:
                print("No valid data found for {0}".format(channel_name))
                sys.stdout.flush()
    except Exception as e:
        print("Error in mbc_epg function for {0}: {1}".format(code, e))
        sys.stdout.flush()
    finally:
        lock.release()
def main():
    print('**************MBC_EPG******************')
    sleep(1)
    print("=================================================")
    print("There are {0} channels available for EPG data.".format(len(channels_code)))
    print("=================================================")
    sleep(1)
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
    sys.stdout.flush()