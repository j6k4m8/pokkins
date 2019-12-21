#!/bin/bash

cd /mnt/vin
python3 -c "from pokkins import Pokkins; print(Pokkins('eps').generate_rss())" > feed.xml
python3 -m http.server 8092
