# Parse the text file created by the scraper into a JSON
# JSON will contain unique ID, media link, post link, caption, number of comments, number of likes etc
# Store JSON to be processed later

import json
import os
import argparse
import sys
import re

parser = argparse.ArgumentParser()
parser.add_argument("--infile")
parser.add_argument("--outfile")
args = parser.parse_args()

fp = open(args.infile)

hdr_to_key = {
				"'Id:": "media_id",
				"Shortcode:": "shortcode",
				"Created at:": "timestamp",
				"Caption:": "caption",
				"Number of comments:": "num_comments",
				"Number of likes:": "num_likes",
				"Link:": "post_link",
				"Hig res image:": "media_link",
				"Media type:": "media_type",				
				"Id": "account_id"
			 }

metadata = []
image_info = {}
caption_str = ""
reading_caption = 0
num_media =  0

# Hashtags regex - taken from rarcega/instagram-scraper
hashtag_regex_string = r"(?<!&)#(\w+|(?:[\xA9\xAE\u203C\u2049\u2122\u2139\u2194-\u2199\u21A9\u21AA\u231A\u231B\u2328\u2388\u23CF\u23E9-\u23F3\u23F8-\u23FA\u24C2\u25AA\u25AB\u25B6\u25C0\u25FB-\u25FE\u2600-\u2604\u260E\u2611\u2614\u2615\u2618\u261D\u2620\u2622\u2623\u2626\u262A\u262E\u262F\u2638-\u263A\u2648-\u2653\u2660\u2663\u2665\u2666\u2668\u267B\u267F\u2692-\u2694\u2696\u2697\u2699\u269B\u269C\u26A0\u26A1\u26AA\u26AB\u26B0\u26B1\u26BD\u26BE\u26C4\u26C5\u26C8\u26CE\u26CF\u26D1\u26D3\u26D4\u26E9\u26EA\u26F0-\u26F5\u26F7-\u26FA\u26FD\u2702\u2705\u2708-\u270D\u270F\u2712\u2714\u2716\u271D\u2721\u2728\u2733\u2734\u2744\u2747\u274C\u274E\u2753-\u2755\u2757\u2763\u2764\u2795-\u2797\u27A1\u27B0\u27BF\u2934\u2935\u2B05-\u2B07\u2B1B\u2B1C\u2B50\u2B55\u3030\u303D\u3297\u3299]|\uD83C[\uDC04\uDCCF\uDD70\uDD71\uDD7E\uDD7F\uDD8E\uDD91-\uDD9A\uDE01\uDE02\uDE1A\uDE2F\uDE32-\uDE3A\uDE50\uDE51\uDF00-\uDF21\uDF24-\uDF93\uDF96\uDF97\uDF99-\uDF9B\uDF9E-\uDFF0\uDFF3-\uDFF5\uDFF7-\uDFFF]|\uD83D[\uDC00-\uDCFD\uDCFF-\uDD3D\uDD49-\uDD4E\uDD50-\uDD67\uDD6F\uDD70\uDD73-\uDD79\uDD87\uDD8A-\uDD8D\uDD90\uDD95\uDD96\uDDA5\uDDA8\uDDB1\uDDB2\uDDBC\uDDC2-\uDDC4\uDDD1-\uDDD3\uDDDC-\uDDDE\uDDE1\uDDE3\uDDEF\uDDF3\uDDFA-\uDE4F\uDE80-\uDEC5\uDECB-\uDED0\uDEE0-\uDEE5\uDEE9\uDEEB\uDEEC\uDEF0\uDEF3]|\uD83E[\uDD10-\uDD18\uDD80-\uDD84\uDDC0]|(?:0\u20E3|1\u20E3|2\u20E3|3\u20E3|4\u20E3|5\u20E3|6\u20E3|7\u20E3|8\u20E3|9\u20E3|#\u20E3|\\*\u20E3|\uD83C(?:\uDDE6\uD83C(?:\uDDEB|\uDDFD|\uDDF1|\uDDF8|\uDDE9|\uDDF4|\uDDEE|\uDDF6|\uDDEC|\uDDF7|\uDDF2|\uDDFC|\uDDE8|\uDDFA|\uDDF9|\uDDFF|\uDDEA)|\uDDE7\uD83C(?:\uDDF8|\uDDED|\uDDE9|\uDDE7|\uDDFE|\uDDEA|\uDDFF|\uDDEF|\uDDF2|\uDDF9|\uDDF4|\uDDE6|\uDDFC|\uDDFB|\uDDF7|\uDDF3|\uDDEC|\uDDEB|\uDDEE|\uDDF6|\uDDF1)|\uDDE8\uD83C(?:\uDDF2|\uDDE6|\uDDFB|\uDDEB|\uDDF1|\uDDF3|\uDDFD|\uDDF5|\uDDE8|\uDDF4|\uDDEC|\uDDE9|\uDDF0|\uDDF7|\uDDEE|\uDDFA|\uDDFC|\uDDFE|\uDDFF|\uDDED)|\uDDE9\uD83C(?:\uDDFF|\uDDF0|\uDDEC|\uDDEF|\uDDF2|\uDDF4|\uDDEA)|\uDDEA\uD83C(?:\uDDE6|\uDDE8|\uDDEC|\uDDF7|\uDDEA|\uDDF9|\uDDFA|\uDDF8|\uDDED)|\uDDEB\uD83C(?:\uDDF0|\uDDF4|\uDDEF|\uDDEE|\uDDF7|\uDDF2)|\uDDEC\uD83C(?:\uDDF6|\uDDEB|\uDDE6|\uDDF2|\uDDEA|\uDDED|\uDDEE|\uDDF7|\uDDF1|\uDDE9|\uDDF5|\uDDFA|\uDDF9|\uDDEC|\uDDF3|\uDDFC|\uDDFE|\uDDF8|\uDDE7)|\uDDED\uD83C(?:\uDDF7|\uDDF9|\uDDF2|\uDDF3|\uDDF0|\uDDFA)|\uDDEE\uD83C(?:\uDDF4|\uDDE8|\uDDF8|\uDDF3|\uDDE9|\uDDF7|\uDDF6|\uDDEA|\uDDF2|\uDDF1|\uDDF9)|\uDDEF\uD83C(?:\uDDF2|\uDDF5|\uDDEA|\uDDF4)|\uDDF0\uD83C(?:\uDDED|\uDDFE|\uDDF2|\uDDFF|\uDDEA|\uDDEE|\uDDFC|\uDDEC|\uDDF5|\uDDF7|\uDDF3)|\uDDF1\uD83C(?:\uDDE6|\uDDFB|\uDDE7|\uDDF8|\uDDF7|\uDDFE|\uDDEE|\uDDF9|\uDDFA|\uDDF0|\uDDE8)|\uDDF2\uD83C(?:\uDDF4|\uDDF0|\uDDEC|\uDDFC|\uDDFE|\uDDFB|\uDDF1|\uDDF9|\uDDED|\uDDF6|\uDDF7|\uDDFA|\uDDFD|\uDDE9|\uDDE8|\uDDF3|\uDDEA|\uDDF8|\uDDE6|\uDDFF|\uDDF2|\uDDF5|\uDDEB)|\uDDF3\uD83C(?:\uDDE6|\uDDF7|\uDDF5|\uDDF1|\uDDE8|\uDDFF|\uDDEE|\uDDEA|\uDDEC|\uDDFA|\uDDEB|\uDDF4)|\uDDF4\uD83C\uDDF2|\uDDF5\uD83C(?:\uDDEB|\uDDF0|\uDDFC|\uDDF8|\uDDE6|\uDDEC|\uDDFE|\uDDEA|\uDDED|\uDDF3|\uDDF1|\uDDF9|\uDDF7|\uDDF2)|\uDDF6\uD83C\uDDE6|\uDDF7\uD83C(?:\uDDEA|\uDDF4|\uDDFA|\uDDFC|\uDDF8)|\uDDF8\uD83C(?:\uDDFB|\uDDF2|\uDDF9|\uDDE6|\uDDF3|\uDDE8|\uDDF1|\uDDEC|\uDDFD|\uDDF0|\uDDEE|\uDDE7|\uDDF4|\uDDF8|\uDDED|\uDDE9|\uDDF7|\uDDEF|\uDDFF|\uDDEA|\uDDFE)|\uDDF9\uD83C(?:\uDDE9|\uDDEB|\uDDFC|\uDDEF|\uDDFF|\uDDED|\uDDF1|\uDDEC|\uDDF0|\uDDF4|\uDDF9|\uDDE6|\uDDF3|\uDDF7|\uDDF2|\uDDE8|\uDDFB)|\uDDFA\uD83C(?:\uDDEC|\uDDE6|\uDDF8|\uDDFE|\uDDF2|\uDDFF)|\uDDFB\uD83C(?:\uDDEC|\uDDE8|\uDDEE|\uDDFA|\uDDE6|\uDDEA|\uDDF3)|\uDDFC\uD83C(?:\uDDF8|\uDDEB)|\uDDFD\uD83C\uDDF0|\uDDFE\uD83C(?:\uDDF9|\uDDEA)|\uDDFF\uD83C(?:\uDDE6|\uDDF2|\uDDFC))))[\ufe00-\ufe0f\u200d]?)+"

for l in fp:
	num_media += 1	
	line = l.lstrip()	
	# else

	if(reading_caption == 1 and (not line.startswith("Number of comments:"))):
		caption_str += line
		continue

	if(line.startswith("Media Info:")):				
		pass
	elif(line.startswith("'Id:")):
		hdr_str = "'Id:"
		line = line.strip(hdr_str).lstrip()
		image_info[hdr_to_key[hdr_str]] = int(line.strip())
	elif(line.startswith("Shortcode:")):
		hdr_str = "Shortcode:"
		line = line.strip(hdr_str).lstrip()
		image_info[hdr_to_key[hdr_str]] = line.strip()
	elif(line.startswith("Created at:")):
		hdr_str = "Created at:"
		line = line.strip(hdr_str).lstrip()
		image_info[hdr_to_key[hdr_str]] = int(line.strip())
	elif(line.startswith("Caption:")):
		if(reading_caption == 1):
			caption_str += line
			continue
		hdr_str = "Caption:"
		reading_caption = 1
		line = line.strip(hdr_str).lstrip()
		caption_str += line		
	elif(line.startswith("Number of comments:")):
		reading_caption = 0
		image_info["caption"] = caption_str
		image_info["hashtags"] = re.findall(hashtag_regex_string, caption_str, re.UNICODE)
		image_info["hashtags"] = list(set(image_info["hashtags"]))
		caption_str = ""
		hdr_str = "Number of comments:"
		line = line.strip(hdr_str).lstrip()
		image_info[hdr_to_key[hdr_str]] = int(line.strip())
	elif(line.startswith("Number of likes:")):
		hdr_str = "Number of likes:"
		line = line.strip(hdr_str).lstrip()
		image_info[hdr_to_key[hdr_str]] = int(line.strip())
	elif(line.startswith("Link:")):
		hdr_str = "Link:"
		line = line.strip(hdr_str).lstrip()
		image_info[hdr_to_key[hdr_str]] = line.strip()
	elif(line.startswith("Hig res image:")):
		hdr_str = "Hig res image:"
		line = line.strip(hdr_str).lstrip()
		image_info[hdr_to_key[hdr_str]] = line.strip()
	elif(line.startswith("Media type:")):
		hdr_str = "Media type:"
		line = line.strip("Media").lstrip().strip("type:").lstrip()		
		image_info[hdr_to_key[hdr_str]] = line.strip()
	elif(line.startswith("Account info:")):
		pass		
	elif(line.startswith("Id")):
		hdr_str = "Id"
		line = line.strip(hdr_str).lstrip()
		image_info[hdr_to_key[hdr_str]] = int(line.strip())
	elif(line.startswith("--------------------------------------------------")):		
		metadata.append(image_info)
		image_info = {}	

fp.close()

with open(args.outfile, 'w') as outfile:
	images_json = {"media_metadata": metadata}
	json.dump(images_json, outfile, indent=4)