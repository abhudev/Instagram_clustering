# Create JSON with just list of image links
# Take as input JSON of structured metadata

import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--jsonfile')
parser.add_argument('--outfile')
args = parser.parse_args()

fp = open(args.jsonfile, 'r')

media_json = json.load(fp)

img_links = []

for media in media_json["media_metadata"]:
	if(media["media_type"] == "image"):
		img_links.append(media["media_link"])

fp.close()

with open(args.outfile, 'w') as fo:
	links_json = {"img_links": img_links}
	json.dump(links_json, fo, indent=4)

