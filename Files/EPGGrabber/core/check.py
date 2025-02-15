#!/usr/bin/python
# -*- coding: utf-8 -*-

from Plugins.Extensions.EPGGrabber.core.compat import PY3

import os
import io
import requests
import sys
if not os.path.exists('/etc/epgimport/ziko_config/custom.channels.xml'):
    print('Downloading custom.channels config')
    sys.stdout.flush()
    custom_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/custom.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/custom.channels.xml', 'w', encoding="utf-8") as f:
        f.write(custom_channels.text)

if not os.path.exists('/etc/epgimport/custom.sources.xml'):
    print('Downloading custom sources config')
    sys.stdout.flush()
    custom_source = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/custom.sources.xml?raw=true')
    with io.open('/etc/epgimport/custom.sources.xml', 'w', encoding="utf-8") as f:
        f.write(custom_source.text)

if not os.path.exists('/etc/epgimport/ziko_config/bein.channels.xml'):
    print('Downloading bein.channels config')
    sys.stdout.flush()
    bein_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/bein.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/bein.channels.xml', 'w', encoding="utf-8") as f:
        f.write(bein_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/elcinema.channels.xml'):
    print('Downloading elcinema channels config')
    sys.stdout.flush()
    elcinema_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/elcinema.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/elcinema.channels.xml', 'w', encoding="utf-8") as f:
        f.write(elcinema_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/egypt2iet5.channels.xml'):
    print('Downloading egypt2iet5 channels config')
    sys.stdout.flush()
    egypt2iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/egypt2iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/egypt2iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(egypt2iet5_channels.text) 

if not os.path.exists('/etc/epgimport/ziko_config/uae1iet5.channels.xml'):
    print('Downloading uae1iet5 channels config')
    sys.stdout.flush()
    uae1iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/uae1iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/uae1iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(uae1iet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/uae2iet5.channels.xml'):
    print('Downloading uae2iet5 channels config')
    sys.stdout.flush()
    uae2iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/uae2iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/uae2iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(uae2iet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/uae3iet5.channels.xml'):
    print('Downloading uae3iet5 channels config')
    sys.stdout.flush()
    uae3iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/uae3iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/uae3iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(uae3iet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/uae4iet5.channels.xml'):
    print('Downloading uae4iet5 channels config')
    sys.stdout.flush()
    uae4iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/uae4iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/uae4iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(uae4iet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/Saudiarabia1iet5.channels.xml'):
    print('Downloading Saudiarabia1iet5 channels config')
    sys.stdout.flush()
    Saudiarabia1iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/Saudiarabia1iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/Saudiarabia1iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(Saudiarabia1iet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/Saudiarabia2iet5.channels.xml'):
    print('Downloading Saudiarabia2iet5 channels config')
    sys.stdout.flush()
    Saudiarabia2iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/Saudiarabia2iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/Saudiarabia2iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(Saudiarabia2iet5_channels.text)        
        
if not os.path.exists('/etc/epgimport/ziko_config/Saudiarabia3iet5.channels.xml'):
    print('Downloading Saudiarabia3iet5 channels config')
    sys.stdout.flush()
    Saudiarabia3iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/Saudiarabia3iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/Saudiarabia3iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(Saudiarabia3iet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/Saudiarabia4iet5.channels.xml'):
    print('Downloading Saudiarabia4iet5 channels config')
    sys.stdout.flush()
    Saudiarabia4iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/Saudiarabia4iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/Saudiarabia4iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(Saudiarabia4iet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/qatar1iet5.channels.xml'):
    print('Downloading qatar1iet5 channels config')
    sys.stdout.flush()
    qatar1iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/qatar1iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/qatar1iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(qatar1iet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/qatar2iet5.channels.xml'):
    print('Downloading qatar2iet5 channels config')
    sys.stdout.flush()
    qatar2iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/qatar2iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/qatar2iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(qatar2iet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/qatar3iet5.channels.xml'):
    print('Downloading qatar3iet5 channels config')
    sys.stdout.flush()
    qatar3iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/qatar3iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/qatar3iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(qatar3iet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/qatar4iet5.channels.xml'):
    print('Downloading qatar4iet5 channels config')
    sys.stdout.flush()
    qatar4iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/qatar4iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/qatar4iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(qatar4iet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/poland1iet5.channels.xml'):
    print('Downloading poland1iet5 channels config')
    sys.stdout.flush()
    poland1iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/poland1iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/poland1iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(poland1iet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/poland2iet5.channels.xml'):
    print('Downloading poland2iet5 channels config')
    sys.stdout.flush()
    poland2iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/poland2iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/poland2iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(poland2iet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/dstv.channels.xml'):
    print('Downloading dstv channels config')
    sys.stdout.flush()
    dstv_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/dstv.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/dstv.channels.xml', 'w', encoding="utf-8") as f:
        f.write(dstv_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/freesat.channels.xml'):
    print('Downloading freesat channels config')
    sys.stdout.flush()
    free_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/freesat.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/freesat.channels.xml', 'w', encoding="utf-8") as f:
        f.write(free_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/skyit.channels.xml'):
    print('Downloading skyit channels config')
    sys.stdout.flush()
    sky_it = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/skyit.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/skyit.channels.xml', 'w', encoding="utf-8") as f:
        f.write(sky_it.text)

if not os.path.exists('/etc/epgimport/ziko_config/discovery.channels.xml'):
    print('Downloading discovery.channels config')
    sys.stdout.flush()
    discovery_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/discovery.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/discovery.channels.xml', 'w', encoding="utf-8") as f:
        f.write(discovery_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/snrt.channels.xml'):
    print('Downloading Snrt.channels config')
    sys.stdout.flush()
    snrt_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/snrt.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/snrt.channels.xml', 'w', encoding="utf-8") as f:
        f.write(snrt_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/satTv.channels.xml'):
    print('Downloading satTv.channels config')
    sys.stdout.flush()
    satTv_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/satTv.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/satTv.channels.xml', 'w', encoding="utf-8") as f:
        f.write(satTv_channels.text)