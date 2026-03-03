# -*- coding: utf-8 -*-

import os
import time
import cloudscraper
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

CHANNELS = {
    "431": "Rotana Cinema KSA",
    "439": "Rotana Cinema Masr",
    "437": "Rotana Comedy",
    "438": "Rotana Classic",
    "436": "Rotana Drama",
    "435": "Rotana Khalijea HD",
    "434": "LBC",
    "443": "Rotana Clip",
    "446": "Al Resalah"
}

TZ = "-120"          # نفس اللي ظهر عندك في XHR
XML_TZ = "+0100"     # مثل سكربتك القديم
OUT_PATH = os.path.join("Files", "rotana.xml")

def fetch_channel_html(scraper, ch_id, retries=3):
    url = f"https://rotana.net/ar/streams?channel={ch_id}&tz={TZ}"
    last_err = None
    for _ in range(retries):
        try:
            r = scraper.get(url, timeout=30)
            if r.status_code == 200:
                return r.text
            last_err = f"HTTP {r.status_code}"
        except Exception as e:
            last_err = str(e)
        time.sleep(2)
    raise RuntimeError(f"Failed to fetch channel {ch_id}: {last_err}")

def parse_programs(html):
    soup = BeautifulSoup(html, "html.parser")
    programs = soup.find_all("h5")
    result = []

    if not programs:
        return result

    current_date = datetime.today()
    prev_time = None

    for i, p in enumerate(programs):
        spans = p.find_all("span")
        if len(spans) < 2:
            continue

        time_str = spans[0].get_text(strip=True)  # HH:MM
        title = spans[1].get_text(strip=True)

        prog_time = datetime.strptime(time_str, "%H:%M").time()
        if prev_time and prog_time < prev_time:
            current_date += timedelta(days=1)

        start = datetime.combine(current_date, prog_time)

        if i < len(programs) - 1:
            ns = programs[i + 1].find_all("span")
            if ns:
                next_time = datetime.strptime(ns[0].get_text(strip=True), "%H:%M").time()
                if next_time < prog_time:
                    stop = datetime.combine(current_date + timedelta(days=1), next_time)
                else:
                    stop = datetime.combine(current_date, next_time)
            else:
                stop = start + timedelta(hours=1)
        else:
            stop = start + timedelta(hours=1)

        result.append((start, stop, title))
        prev_time = prog_time

    return result

def build_xml(all_data):
    tv = ET.Element("tv", attrib={"generator-info-name": "Rotana EPG (GitHub Actions)"})

    # channels section
    for ch_id, ch_name in CHANNELS.items():
        ch = ET.SubElement(tv, "channel", attrib={"id": ch_id})
        dn = ET.SubElement(ch, "display-name", attrib={"lang": "ar"})
        dn.text = ch_name

    # programmes section
    for ch_id, items in all_data.items():
        for start, stop, title in items:
            pr = ET.SubElement(tv, "programme", attrib={
                "start": start.strftime(f"%Y%m%d%H%M%S {XML_TZ}"),
                "stop":  stop.strftime(f"%Y%m%d%H%M%S {XML_TZ}"),
                "channel": ch_id
            })
            t = ET.SubElement(pr, "title", attrib={"lang": "ar"})
            t.text = title
            d = ET.SubElement(pr, "desc", attrib={"lang": "ar"})
            d.text = "وصف غير متوفر"

    return ET.ElementTree(tv)

def main():
    os.makedirs("Files", exist_ok=True)

    scraper = cloudscraper.create_scraper(
        browser={"browser": "chrome", "platform": "windows", "mobile": False}
    )

    all_data = {}
    for ch_id in CHANNELS.keys():
        html = fetch_channel_html(scraper, ch_id)
        all_data[ch_id] = parse_programs(html)

    tree = build_xml(all_data)
    tree.write(OUT_PATH, encoding="utf-8", xml_declaration=True)

    print(f"OK: wrote {OUT_PATH}")

if __name__ == "__main__":
    main()
