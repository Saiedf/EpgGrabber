#!/bin/sh

# Clear the cache memory
echo 1 > /proc/sys/vm/drop_caches
echo 2 > /proc/sys/vm/drop_caches
echo 3 > /proc/sys/vm/drop_caches

# Execute the Python scripts sequentially
python /usr/lib/enigma2/python/Plugins/Extensions/EPGGrabber/providers/elcinmaiet5.py &
wait
python /usr/lib/enigma2/python/Plugins/Extensions/EPGGrabber/providers/beinsportiet5.py &
wait
python /usr/lib/enigma2/python/Plugins/Extensions/EPGGrabber/providers/nilesatiet5.py &
wait
python /usr/lib/enigma2/python/Plugins/Extensions/EPGGrabber/providers/sportiet5.py &
wait
python /usr/lib/enigma2/python/Plugins/Extensions/EPGGrabber/providers/uaeariet5.py &
wait
python /usr/lib/enigma2/python/Plugins/Extensions/EPGGrabber/providers/uaeeniet5.py &
wait
python /usr/lib/enigma2/python/Plugins/Extensions/EPGGrabber/providers/beincin.py &
wait
python /usr/lib/enigma2/python/Plugins/Extensions/EPGGrabber/providers/beinConnect.py &
wait
python /usr/lib/enigma2/python/Plugins/Extensions/EPGGrabber/providers/elcin.py &
wait
python /usr/lib/enigma2/python/Plugins/Extensions/EPGGrabber/providers/elcinEN.py &
wait

# Exit the script
exit 0