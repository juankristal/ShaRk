import requests
from io import StringIO
import os
import re
from time import time

def getOsuFile(beatmap_id):

    cached_maps=os.listdir("./cached_maps/")
    if beatmap_id+".osu" in cached_maps: 
        print("cached")
        return open(f'./cached_maps/{beatmap_id}.osu', mode='r',encoding="utf-8")
    else:
        s = StringIO(requests.get(f"https://osu.ppy.sh/osu/{beatmap_id}").content.decode("utf-8"))
        with open(f'./cached_maps/{beatmap_id}.osu', mode='w',newline='',encoding="utf-8") as f:
           f.write(s.read())
        return s

    

def extractBeatmapIds(text):
	r = re.findall(r'(?:/b/\d+)|(?:#mania/\d+)|(?:[\s;,\n]\d\d\d\d\d+[\s;,\n])|(?:beatmaps/\d+)', text)
	r = re.findall(r'\d+', " ".join(r))
	return r