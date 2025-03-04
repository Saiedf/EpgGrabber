# -*- coding: utf-8 -*-
import sys
import os
import requests
from bs4 import BeautifulSoup
import io
from datetime import datetime, timedelta
import json

# Import from the same directory
from __init__ import *

print(u'************** Rotana EPG ******************')

# List of channels
channels = [
    "431-Rotana Cinema KSA", "439-Rotana Cinema Masr", "437-Rotana Comedy", 
    "438-Rotana Classic", "436-Rotana Drama", "435-Rotana Khalijea HD", 
    "434-LBC", "443-Rotana Clip", "446-Al Resalah"
]

# HTTP headers for requests
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'}

# Function to write the XML header
def xml_header(file_path, channels):
    with io.open(file_path, "w", encoding='UTF-8') as f:
        f.write(u'<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(u'<tv generator-info-name="By ZR1">\n')
        
        for channel in channels:
            channel_id = channel.split('-')[1]
            f.write(u'  <channel id="{}">\n'.format(channel_id))
            f.write(u'    <display-name lang="en">{}</display-name>\n'.format(channel_id))
            f.write(u'  </channel>\n')

# Function to close the XML file
def close_xml(file_path):
    with io.open(file_path, "a", encoding='UTF-8') as f:
        f.write(u'</tv>\n')

# Function to fetch EPG data for a channel
def fetch_epg_for_channel(channel_id):
    url = "https://rotana.net/ar/streams?channel={}&tz=".format(channel_id)
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(u"خطأ في تحميل البيانات للقناة {}".format(channel_id))
            return []
        soup = BeautifulSoup(response.text, 'html.parser')
        epg_data = []
        date_element = soup.find('h4', class_='big-title text-uppercase mt-0 fadeInRight animated')
        if date_element:
            current_date_str = date_element.get_text(strip=True)
            date_part = current_date_str[-10:]
            current_date = datetime.strptime(date_part, "%Y-%m-%d")
        else:
            print(u"لم يتم العثور على تاريخ اليوم.")
            return []
        programs = soup.find_all('h5', class_='big-title text-uppercase mt-0 fadeInLeft animated')
        previous_time = None
        next_start_time = None
        for i, program in enumerate(programs):
            time_str = program.find('span').get_text(strip=True)
            program_name = program.find_all('span')[1].get_text(strip=True)
            program_time = datetime.strptime(time_str, "%H:%M").time()
            if previous_time and program_time < previous_time:
                current_date += timedelta(days=1)
            start_time = datetime.combine(current_date, program_time)
            if i < len(programs) - 1:
                next_time_str = programs[i + 1].find('span').get_text(strip=True)
                next_program_time = datetime.strptime(next_time_str, "%H:%M").time()
                if next_program_time < program_time:
                    next_start_time = datetime.combine(current_date + timedelta(days=1), next_program_time)
                else:
                    next_start_time = datetime.combine(current_date, next_program_time)
            else:
                next_start_time = start_time + timedelta(hours=1)
            epg_data.append({
                'start': start_time.strftime('%Y%m%d%H%M%S'),
                'end': next_start_time.strftime('%Y%m%d%H%M%S'),
                'title': program_name,
                'description': u"وصف غير متوفر"
            })
            previous_time = program_time
        return epg_data
    except Exception as e:
        print(u"خطأ أثناء جلب البيانات: {}".format(str(e)))
        return []

# Function to write EPG data to XML
def Toxml(epg_data, channel_name):
    time_zone = "+0100"  # المنطقة الزمنية كما هو مطلوب
    channel_id = channel_name.split('-')[1]
    for program in epg_data:
        ch = u''
        start_time_xml = program['start']
        end_time_xml = program['end']
        ch += 2 * u' ' + u'<programme start="{} {}" stop="{} {}" channel="{}">\n'.format(
            start_time_xml, time_zone, end_time_xml, time_zone, channel_id
        )
        ch += 4 * u' ' + u'<title lang="ar">{}</title>\n'.format(
            program["title"].replace("&#39;", "'").replace("&quot;", '"').replace("&amp;", "&")
        )
        ch += 4 * u' ' + u'<desc lang="ar">{}</desc>\n'.format(
            program["description"].replace("&#39;", "'").replace("&quot;", '"').replace("&amp;", "&").strip()
        )
        ch += 2 * u' ' + u'</programme>\r'
        with io.open(EPG_ROOT + '/rotana.xml', "a", encoding='UTF-8') as f:
            f.write(ch)  # Write Unicode string directly
    if epg_data:
        last_program_time = datetime.strptime(epg_data[-1]['start'], '%Y%m%d%H%M%S')
        formatted_time = last_program_time.strftime('%Y-%m-%d %H:%M')
        print(u"{} epg ends at : {}".format(channel_id, formatted_time))
    else:
        print(u"{} epg ends at : No data available".format(channel_id))
    sys.stdout.flush()

# Main function
def main():
    try:
        with open(PROVIDERS_ROOT, 'r') as f:
            data = json.load(f)
        for channel in data['bouquets']:
            if channel["bouquet"] == "rotana":
                channel['date'] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
        with open(PROVIDERS_ROOT, 'w') as f:
            json.dump(data, f)
        
        xml_header(EPG_ROOT + '/rotana.xml', channels)
        for channel in channels:
            parts = channel.split('-', 1)
            channel_id = parts[0]
            channel_name = parts[1]
            epg_data = fetch_epg_for_channel(channel_id)
            Toxml(epg_data, channel)
        close_xml(EPG_ROOT + '/rotana.xml')
        print(u'************** FINISHED ******************')
    except Exception as e:
        print(u"خطأ في الدالة الرئيسية: {}".format(str(e)))

# Entry point
if __name__ == "__main__":
    main()
    
    sys.stdout.flush()