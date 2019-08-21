from pathlib import Path
import subprocess

#dn1 is a pandas frame with channel names and ids created from the yt_channel_scraper.py script. 
#old_channels is a frame containing channels that have already been downloaded
xxx=[]
dnew_p = pd.DataFrame()
for i,w in dn1.iterrows():
    if not w["channel_id"] in old_channels["channel_id"]:
            result = subprocess.run(["youtube-dl",
            "https://www.youtube.com/channel/"+w["channel_id"],
            "--skip-download",
            "--get-title",
            "--get-id",
            "--verbose"],
             stdout=subprocess.PIPE)
            proc = result.stdout
            if proc:
                groups = proc.split(b'\n')
                for x,y in zip(groups[1::3], groups[2::3]):
                    if x not in xxx:
                            dnew_p= dnew_p.append([[w["state"],w["search_term"],
                                                  w["channel_title"],w["channel_id"],
                                                x.decode('utf-8'),y.decode('utf-8')]])
                            result1 = subprocess.run(["youtube-dl",
                                "--skip-download",
                                "--write-auto-sub",
                                "--sub-lang",
                                "en",
                                "https://youtu.be/"+y.decode('utf-8'),
                                "-o",
                                "/path/to/storage%s"% w["state"]+"/%s"% w["channel_title"]+"/%(title)s.%(ext)s" ],
                                     stdout=subprocess.PIPE)
                            proc1 = result.stdout
                            xxx.extend(x)

dnew_p.reset_index(drop=True)
dnew_p.columns = ["state","search_term","channel_name","channel_id","video_title","video_id"]

import re
import pandas as pd
import html5lib
from bs4 import BeautifulSoup
import webvtt

def remove_adjacent(nums):
     return [a for a,b in zip(nums, nums[1:]+[not nums[-1]]) if a != b]
    
def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)

dnp_good=pd.DataFrame()
for i,x in dnew_p.iterrows():
    vid = "/path/to/storage%s/%s/%s"%(x["state"],x["channel_name"],x["video_title"])+".en.vtt"
    vid1 = re.sub("\:"," -",vid)
    try:
        stripped1=[]
        time = []
        time1 = []
        captions = webvtt.read(vid1)
        for caption in captions:
            stripped = caption.text.replace('\n', "\n")
            stripped1.append(stripped.split("\n"))
            gg = [x for y in stripped1 for x in y if x != " "]
            gg1 = " ".join(remove_adjacent(gg))
            caption1 = re.sub("\n","",caption.text)
            #print(caption1)
            if not re.search("^\s*$|^\s*\[Applause\]$|^\s*\[Music\]$|^\s*\[Laughter\]$",caption1):
                time.append(get_sec(caption.end)-get_sec(caption.start))
                
            time1 = sum(time)
            #print(time1)

        dnp_good=dnp_good.append([[x["state"],x["search_term"],x["channel_name"],x["channel_id"],
                           x["video_title"],x["video_id"],gg1,time1]])
    except:
        continue
        
dnp_good.columns = ["state","search_term","channel_name","channel_id","video_title",
              "video_id","text","speech_duration"]
