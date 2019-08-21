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
