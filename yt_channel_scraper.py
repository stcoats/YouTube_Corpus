#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import argparse

my_cse_id = "" #Add your credentials here
dev_key = "" #Add your credentials here

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

statename_to_abbr = {
    # Other
    'District of Columbia': 'DC',
    
    # States
    'Alabama': 'AL',
    'Montana': 'MT',
    'Alaska': 'AK',
    'Nebraska': 'NE',
    'Arizona': 'AZ',
    'Nevada': 'NV',
    'Arkansas': 'AR',
    'New Hampshire': 'NH',
    'California': 'CA',
    'New Jersey': 'NJ',
    'Colorado': 'CO',
    'New Mexico': 'NM',
    'Connecticut': 'CT',
    'New York': 'NY',
    'Delaware': 'DE',
    'North Carolina': 'NC',
    'Florida': 'FL',
    'North Dakota': 'ND',
    'Georgia': 'GA',
    'Ohio': 'OH',
    'Hawaii': 'HI',
    'Oklahoma': 'OK',
    'Idaho': 'ID',
    'Oregon': 'OR',
    'Illinois': 'IL',
    'Pennsylvania': 'PA',
    'Indiana': 'IN',
    'Rhode Island': 'RI',
    'Iowa': 'IA',
    'South Carolina': 'SC',
    'Kansas': 'KS',
    'South Dakota': 'SD',
    'Kentucky': 'KY',
    'Tennessee': 'TN',
    'Louisiana': 'LA',
    'Texas': 'TX',
    'Maine': 'ME',
    'Utah': 'UT',
    'Maryland': 'MD',
    'Vermont': 'VT',
    'Massachusetts': 'MA',
    'Virginia': 'VA',
    'Michigan': 'MI',
    'Washington': 'WA',
    'Minnesota': 'MN',
    'West Virginia': 'WV',
    'Mississippi': 'MS',
    'Wisconsin': 'WI',
    'Missouri': 'MO',
    'Wyoming': 'WY',
    'American Samoa':'AS',
    'Guam':'GU',
    'Northern Mariana Islands':'MP',
    'Puerto Rico':'PR',
    'Virgin Islands (U.S.)':'VI',
    'U.S. Minor Outlying Islands':'UM'
}


f = open("/path/to/your/output/file.txt","w")

def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=dev_key)
    search_response = youtube.search().list(
        q=options.q,
        part="id,snippet",
        maxResults=options.max_results
          ).execute()

    videos = []
    channels = []
    playlists = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#channel":
              channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"]))
                                 
    print ("Channels:\n",channels, "\n")
    f.writelines([options.q+"--"+x[0]+"\n" for x in channels])

for y in ["county of","city of", "municipal", "town meeting","city council","county supervisors",
	  "board of supervisors","government"]:
  for x in list(statename_to_abbr.values()):
    if __name__ == "__main__":
      argparser = argparse.ArgumentParser(conflict_handler='resolve')
      argparser.add_argument("--q", help="Search term", default=y+" "+x)
      argparser.add_argument("--max-results", help="Max results", default=25)
      args = argparser.parse_args()
      print(args)
      try:
        youtube_search(args)
      except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
 
f.close()
