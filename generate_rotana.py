# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import urllib.request
import os

channels = [
    ("431", "Rotana Cinema KSA"),
    ("439", "Rotana Cinema Masr"),
    ("437", "Rotana Comedy"),
    ("438", "Rotana Classic"),
    ("436", "Rotana Drama"),
    ("435", "Rotana Khalijea HD"),
    ("434", "LBC"),
    ("443", "Rotana Clip"),
    ("446", "Al Resalah"),
]

GITHUB_BACKUP = "https://raw.githubusercontent.com/Saiedf/EpgGrabber/main/Files/rotana.xml"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_channel(channel_id):
    url = "https://rotana.net/ar/streams?channel={}&tz=-120".format(channel_id)
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return None

        soup = BeautifulSoup(r.text, "html.parser")
        programs = soup.find_all("h5")

        if not programs:
            return None

        epg = []
        current_date = datetime.today()
        previous_time = None

        for i, p in enumerate(programs):
            spans = p.find_all("span")
            if len(spans) < 2:
                continue

            time_str = spans[0].get_text(strip=True)
            title = spans[1].get_text(strip=True)

            prog_time = datetime.strptime(time_str, "%H:%M").time()

            if previous_time and prog_time < previous_time:
                current_date += timedelta(days=1)

            start_dt = datetime.combine(current_date, prog_time)

            if i < len(programs) - 1:
                next_spans = programs[i + 1].find_all("span")
                if next_spans:
                    next_time = datetime.strptime(
                        next_spans[0].get_text(strip=True), "%H:%M"
                    ).time()
                    if next_time < prog_time:
                        stop_dt = datetime.combine(current_date + timedelta(days=1), next_time)
                    else:
                        stop_dt = datetime.combine(current_date, next_time)
                else:
                    stop_dt = start_dt + timedelta(hours=2)
            else:
                stop_dt = start_dt + timedelta(hours=2)

            epg.append((start_dt, stop_dt, title))
            previous_time = prog_time

        return epg

    except:
        return None


def fallback_from_github():
    print("Using GitHub backup XML")
    urllib.request.urlretrieve(GITHUB_BACKUP, "Files/rotana.xml")


def main():
    root = ET.Element("tv", attrib={"generator-info-name": "By ZR1"})
    all_data = {}
    failed = False

    for ch_id, ch_name in channels:
        data = fetch_channel(ch_id)
        if data is None:
            failed = True
            break
        all_data[ch_id] = data

    if failed:
        fallback_from_github()
        return

    for ch_id, ch_name in channels:
        ch = ET.SubElement(root, "channel", attrib={"id": ch_name})
        dn = ET.SubElement(ch, "display-name", attrib={"lang": "en"})
        dn.text = ch_name

    for ch_id, ch_name in channels:
        for start_dt, stop_dt, title in all_data.get(ch_id, []):
            pr = ET.SubElement(root, "programme", attrib={
                "start": start_dt.strftime("%Y%m%d%H%M%S +0200"),
                "stop": stop_dt.strftime("%Y%m%d%H%M%S +0200"),
                "channel": ch_name
            })
            t = ET.SubElement(pr, "title", attrib={"lang": "ar"})
            t.text = title
            d = ET.SubElement(pr, "desc", attrib={"lang": "ar"})
            d.text = "Description not available"

    tree = ET.ElementTree(root)
    tree.write("Files/rotana.xml", encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    main()
