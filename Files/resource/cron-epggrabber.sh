#!/bin/sh

echo 1 > /proc/sys/vm/drop_caches
echo 2 > /proc/sys/vm/drop_caches
echo 3 > /proc/sys/vm/drop_caches


python /usr/lib/enigma2/python/Plugins/Extensions/EPGGrabber/providers/bebawy6.py
wait 
python /usr/lib/enigma2/python/Plugins/Extensions/EPGGrabber/providers/beincin.py
wait
python /usr/lib/enigma2/python/Plugins/Extensions/EPGGrabber/providers/beinConnect.py
wait
python /usr/lib/enigma2/python/Plugins/Extensions/EPGGrabber/providers/elcin.py
wait
python /usr/lib/enigma2/python/Plugins/Extensions/EPGGrabber/providers/elcinEN.py
wait
python /usr/lib/enigma2/python/Plugins/Extensions/EPGGrabber/providers/elcinmaiet5.py
wait
python /usr/lib/enigma2/python/Plugins/Extensions/EPGGrabber/providers/jawwyenOS.py
python /usr/lib/enigma2/python/Plugins/Extensions/EPGGrabber/providers/sportiet5.py

exit 0
