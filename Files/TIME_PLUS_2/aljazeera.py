#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division

# استيراد المكتبات والملفات الضرورية
try:
    from core.__init__ import *  # استيراد المتغيرات والإعدادات من ملف core
except ImportError:
    from __init__ import *
import requests
import re
import io
import sys
import random
import urllib3
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError, RequestException
from bs4 import BeautifulSoup

# Disable SSL warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

# دعم التوافق مع Python 2 و 3
try:
    range = xrange  # Python 2
except NameError:
    pass  # Python 3

print('************ Al Jazeera EPG **************')
sys.stdout.flush()

# قاموس لتحويل أسماء الشهور إلى أرقام
MONTHS = {
    "يناير": "01", "كانون الثاني": "01", "January": "01",
    "فبراير": "02", "شباط": "02", "February": "02",
    "مارس": "03", "آذار": "03", "March": "03",
    "أبريل": "04", "نيسان": "04", "April": "04",
    "مايو": "05", "أيار": "05", "May": "05",
    "يونيو": "06", "حزيران": "06", "June": "06",
    "يوليو": "07", "تموز": "07", "July": "07",
    "أغسطس": "08", "آب": "08", "August": "08",
    "سبتمبر": "09", "أيلول": "09", "September": "09",
    "أكتوبر": "10", "تشرين الأول": "10", "October": "10",
    "نوفمبر": "11", "تشرين الثاني": "11", "November": "11",
    "ديسمبر": "12", "كانون الأول": "12", "December": "12"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "ar,en-US;q=0.7,en;q=0.3",
    "Connection": "keep-alive"
}

def to_xml(data, filename, channel_name, target_date):
    # التحقق من وجود بيانات
    if len(data) > 0:
        ch = ''  # نص البرنامج بتنسيق XML
        for idx, (elem, tit, de) in enumerate(zip(data['times'], data['titles'], data['descriptions'])):
            # تحويل التاريخ والوقت إلى تنسيق صالح
            try:
                start = datetime.strptime(target_date + ' ' + elem, '%Y%m%d %H:%M').strftime('%Y%m%d%H%M%S')
            except ValueError as e:
                print("Error parsing time: {}".format(e))
                continue  # تخطي هذا البرنامج إذا كان الوقت غير صالح
            # تحديد وقت النهاية
            if idx < len(data['times']) - 1:
                next_time = data['times'][idx + 1]
                try:
                    end = datetime.strptime(target_date + ' ' + next_time, '%Y%m%d %H:%M').strftime('%Y%m%d%H%M%S')
                except ValueError as e:
                    print("Error parsing next time: {}".format(e))
                    end = (datetime.strptime(start, '%Y%m%d%H%M%S') + timedelta(hours=1)).strftime('%Y%m%d%H%M%S')
            else:
                end = (datetime.strptime(start, '%Y%m%d%H%M%S') + timedelta(hours=1)).strftime('%Y%m%d%H%M%S')
            # إضافة إزاحة زمنية قدرها 3 ساعات توقيت مصر(+0300)
            start_time = datetime.strptime(start, '%Y%m%d%H%M%S') + timedelta(hours=0)
            end_time = datetime.strptime(end, '%Y%m%d%H%M%S') + timedelta(hours=0)
            # تحويل الأوقات إلى تنسيق صالح
            start = start_time.strftime('%Y%m%d%H%M%S')
            end = end_time.strftime('%Y%m%d%H%M%S')
            # كتابة البيانات بتنسيق XML
            ch += 2 * ' ' + '<programme start="' + start + ' +0300" stop="' + end + ' +0300" channel="' + channel_name + '">\n'
            ch += 4 * ' ' + '<title lang="ar">' + tit.strip() + '</title>\n'
            ch += 4 * ' ' + '<desc lang="ar">' + de.strip() + '</desc>\n'
            ch += 2 * ' ' + '</programme>\r'
        # كتابة النص إلى الملف
        with io.open(filename, "a", encoding="utf-8") as f:
            f.write(ch)
        print("{} EPG for {} downloaded successfully.".format(channel_name, target_date))
        sys.stdout.flush()
    else:
        print("No data found for {} on {}".format(channel_name, target_date))
        sys.stdout.flush()

# دالة لجلب الجدول الزمني للقناة
def fetch_schedule(url, filename, channel_name):
    try:
        with requests.Session() as s:
            # إعدادات خاصة لموقع الجزيرة دوك
            if 'doc.aljazeera.net' in url:
                custom_headers = HEADERS.copy()
                custom_headers.update({ "Host": "doc.aljazeera.net", "Referer": "https://doc.aljazeera.net" })
                # استخدام IP مباشر مع تعطيل SSL
                s.mount('https://', HTTPAdapter(max_retries=5))
                response = s.get("https://104.106.85.66/schedule", headers=custom_headers, verify=False, timeout=30)
            else:
                # إعدادات عادية للمواقع الأخرى
                s.mount('https://', HTTPAdapter(max_retries=3))
                response = s.get(url, headers=HEADERS, timeout=15)
                response.encoding = 'utf-8'  # تأكد من استخدام ترميز UTF-8
                response.raise_for_status()
            if channel_name == 'aljazeera_doc':
                # معالجة بيانات الجزيرة الوثائقية بشكل خاص
                soup = BeautifulSoup(response.text, "html.parser")
                h3_tags = soup.find_all("h3")
                for h3 in h3_tags:
                    # استخراج النص الكامل للتاريخ من العلامة <h3>
                    date_text = h3.text.strip()
                    # تحليل النص لاستخراج اليوم والشهر والسنة
                    try:
                        # استخدام تعبير عادي لاستخراج التاريخ
                        date_match = re.search(r'(\d{1,2})\s+(\S+)\s*(?:/|\s)(\S*)\s+(\d{4})', date_text)
                        if date_match:
                            day = date_match.group(1)  # اليوم (رقم)
                            month_ar = date_match.group(2)  # الشهر (اسم عربي)
                            month_en = date_match.group(3)  # الشهر (اسم إنجليزي، قد يكون فارغًا)
                            year = date_match.group(4)  # السنة
                            month_num = MONTHS.get(month_ar, MONTHS.get(month_en, "01"))  # إذا لم يتم العثور على الشهر، نستخدم "01" كقيمة 
                            # إنشاء تاريخ بتنسيق YYYYMMDD
                            target_date = "{}{}{}".format(year, month_num, day.zfill(2))
                    except Exception as e:
                        print("Error parsing date: {}".format(e))
                        target_date = datetime.today().strftime('%Y%m%d')
                    
                    data = { 'times': [], 'titles': [], 'descriptions': [] }
                    next_sibling = h3.find_next_sibling()
                    while next_sibling and next_sibling.name != 'h3':
                        if next_sibling.name == 'p':
                            programme = next_sibling.text.strip()
                            if programme:
                                time, title = programme.split(None, 1)  # Fixed: Replaced maxsplit=1 with None, 1
                                data['times'].append(time)
                                data['titles'].append(title)
                                data['descriptions'].append("لا يوجد وصف")
                        next_sibling = next_sibling.find_next_sibling()
                   
                    to_xml(data, filename, channel_name, target_date)
            else:
                soup = BeautifulSoup(response.text, "html.parser")
                times = [elem.text.strip() for elem in soup.find_all(class_="schedule__row__timeslot")]
                titles = []
                for elem in soup.find_all(class_="schedule__row__showname"):
                    # Find the "يعرض الآن" element
                    now_showing = elem.find(class_="schedule__row__nowshowing")
                    if now_showing:
                        # Extract "يعرض الآن" and the show name separately
                        now_showing_text = now_showing.text.strip()
                        show_name = elem.text.replace(now_showing_text, "").strip()
                        # Combine them with a single space
                        title = "%s %s" % (now_showing_text, show_name)
                    else:
                        # If "يعرض الآن" doesn't exist, use the show name as is
                        title = elem.text.strip()
                    titles.append(title)
                descriptions = [elem.text.strip() for elem in soup.find_all(class_="schedule__row__description")]
                
                target_date = datetime.today().strftime('%Y%m%d')
                data = {
                    'times': times,
                    'titles': titles,
                    'descriptions': descriptions
                }
                
                to_xml(data, filename, channel_name, target_date)
    except RequestException as e:
        print("Connection error ({}): {}".format(channel_name, str(e)))

def main():
    # Existing code for EPG download
    xml_header(EPG_ROOT + '/aljazeera.xml', ['aljazeera', 'aljazeera_doc'])
    fetch_schedule('https://www.ajnet.me/schedule/', EPG_ROOT + '/aljazeera.xml', 'aljazeera')
    fetch_schedule('https://doc.aljazeera.net/schedule', EPG_ROOT + '/aljazeera.xml', 'aljazeera_doc')
    close_xml(EPG_ROOT + '/aljazeera.xml')
    with open(PROVIDERS_ROOT, 'r') as f:
        data = json.load(f)
    for channel in data['bouquets']:
        if channel["bouquet"] == "aljazeera":
            channel['date'] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
    with open(PROVIDERS_ROOT, 'w') as f:
        json.dump(data, f)


if __name__ == "__main__":
    main()

    print("**************FINISHED******************")
    sys.stdout.flush()