# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import requests, re, sys, json
from datetime import datetime
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
from time import sleep  # Import sleep for delays

# Handle the import of __init__.py
try:
    from .__init__ import *
except (ImportError, ValueError):
    # If the relative import fails, try an absolute import
    try:
        from __init__ import *
    except ImportError:
        # If both imports fail, define EPG_ROOT here or handle the error
        EPG_ROOT = os.path.dirname(os.path.abspath(__file__))

SEPARATOR_LENGTH = 49

def print_separator(title):
    stars = "*" * ((SEPARATOR_LENGTH - len(title) - 2) // 2)
    print("{0} {1} {0}".format(stars, title))
    sys.stdout.flush()  # Flush after printing the separator

channels = {
    name: "https://www.snrt.ma/ar/node/{}".format(num)
    for name, num in zip(
        [ "Al Aoula", "Laâyoune", "Arryadia", "Athaqafia", "Almaghribia", "Assadissa", "Tamazight", "Alidaa alwatania", "Chaine Inter", "Idaât Mohammed Assadiss", "Alidaâ Alamazighia" ], [1208, 4069, 4070, 4071, 4072, 4073, 4075, 4076, 4077, 4078, 4079] ) }

def clean_text(text):
    return ' '.join(text.split()).strip()

def extract_time(time_str):
    time_cleaned = time_str.replace("H", ":").strip()
    match = re.match(r"^(\d{1,2}):(\d{2})$", time_cleaned)
    if match:
        hour, minute = match.groups()
        hour = hour.zfill(2)
        return int(hour), int(minute)
    match = re.search(r"(\d{2}):(\d{2}):\d{2}$", time_cleaned)
    if match:
        hour, minute = map(int, match.groups())
        return hour, minute
    return None

def get_channel_schedule(channel_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Referer": "https://www.snrt.ma/ar"
    }
    try:
        response = requests.get(channel_url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    epg_data = {}
    for div in soup.find_all("div", class_="grille-line"):
        date_class = div.get("class", [])
        day_key = next((c for c in date_class if c.isdigit()), None)
        if not day_key:
            continue
        time_div = div.find("div", class_="grille-time")
        if not time_div:
            continue
        raw_time = time_div.text.strip()
        extracted_time = extract_time(raw_time)
        if not extracted_time:
            continue
        hour, minute = extracted_time
        title = clean_text(div.find("h2", class_="program-title-sm").text)
        desc_div = div.find("div", class_="grille-content")
        raw_desc = clean_text(desc_div.text) if desc_div else ""
        description = raw_desc.replace(title, "").strip() or title
        start_time = "{}{:02}{:02}00 +0000".format(day_key, hour, minute)
        stop_time = "{}{:02}{:02}00 +0000".format(day_key, hour, minute + 5)
        if day_key not in epg_data:
            epg_data[day_key] = []
        if not any(p['title'] == title and p['start'] == start_time for p in epg_data[day_key]):
            epg_data[day_key].append({ "start": start_time, "stop": stop_time, "title": title, "desc": description })
    return epg_data

def generate_xml(all_schedules):
    root = ET.Element("tv")
    root.set("generator-info-name", "SNRT-EPG")
    # Add channels
    for channel_id in channels:
        channel_elem = ET.SubElement(root, "channel", id=channel_id)
        ET.SubElement(channel_elem, "display-name").text = channel_id
    # Add programmes
    end_times = []
    for channel_id, programs in all_schedules.items():
        last_time = None
        for day in sorted(programs.keys()):
            for program in programs[day]:
                prog_elem = ET.SubElement(
                    root,
                    "programme",
                    start=program["start"],
                    stop=program["stop"],
                    channel=channel_id
                )
                ET.SubElement(prog_elem, "title").text = program["title"]
                ET.SubElement(prog_elem, "desc").text = program["desc"]
                try:
                    # Python 3 compatibility
                    last_time = datetime.strptime(program["start"], "%Y%m%d%H%M%S %z")
                except ValueError:
                    # Python 2 fallback
                    dt_str = program["start"].split()[0]
                    last_time = datetime.strptime(dt_str, "%Y%m%d%H%M%S")
        if last_time:
            end_times.append("{} epg ends at: {}".format(
                channel_id, 
                last_time.strftime("%Y-%m-%d %H:%M")
            ))
    # XML formatting
    xml_str = ET.tostring(root, encoding="utf-8")
    if sys.version_info[0] < 3:
        xml_str = xml_str.decode("utf-8")
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")
    return pretty_xml, end_times

def main():
    print('*****************SNRT_EPG*********************')
    sys.stdout.flush()  # Flush after the initial print
    sleep(1)  # Add a 1-second delay
    print("==============================================")
    print("There are {0} channels available for EPG data.".format(len(channels)))
    print("==============================================")
    sys.stdout.flush()  # Flush after printing the channel count
    sleep(1)  # Add a 1-second delay

    #print_separator("SNRT EPG")
    all_schedules = {}
    end_times = []
    for channel_name, url in channels.items():
        #print("Fetching EPG data for {}...".format(channel_name))  # Python 2 compatible format
        sys.stdout.flush()  # Flush after printing the channel name
        epg_data = get_channel_schedule(url)
        if epg_data:
            all_schedules[channel_name] = epg_data
            last_day = sorted(epg_data.keys())[-1]
            last_program = epg_data[last_day][-1]
            try:
                # Python 3 method
                last_time = datetime.strptime(last_program["start"], "%Y%m%d%H%M%S %z")
            except ValueError:
                # Python 2 fallback
                dt_str = last_program["start"].split()[0]
                last_time = datetime.strptime(dt_str, "%Y%m%d%H%M%S")
            end_time_str = "{} epg ends at: {}".format(
                channel_name,
                last_time.strftime("%Y-%m-%d %H:%M")
            )
            end_times.append(end_time_str)
            print(end_time_str)
            sys.stdout.flush()  # Flush after printing the end time
    xml_content, _ = generate_xml(all_schedules)
    with open(EPG_ROOT + '/snrt.xml', "w") as f:
        if sys.version_info[0] < 3:
            xml_content = xml_content.encode("utf-8")
        f.write(xml_content)
    print("*" * SEPARATOR_LENGTH)
    print("SNRT EPG saved successfully!")
    print_separator("FINISHED")
    sys.stdout.flush()  # Flush after finishing

if __name__ == '__main__':
    main()
    sys.stdout.flush()  # Flush after the final print