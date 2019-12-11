# Figure out the hash-tag distribution per cluster obtained by anty kind of clustering

import json
from collections import defaultdict, Counter
import matplotlib.pyplot as plt


with open('climate_igram_10k.json', 'r') as fin:
	img_json = json.load(fin)


categories = []
hashtag_counts = {}

# This file contains k lines where k = number of clusters
# Each line has a list of post names, comma-separated
fp = open('clustered_filename_img.csv', 'r')


for category, line in enumerate(fp):	
	cur_cat = []
	for word in line.split(','):
		cur_cat.append(word)
	categories.append(cur_cat)

def get_v(tup):
	return tup[1]

for i, cat_list in enumerate(categories):
	tag_dict = Counter()
	with open(f'cat_{i}_img.txt', 'w') as fout:
		for im in cat_list:
			# print(f"im {im}")
			for media in img_json['media_metadata']:
				cur_im = media['media_link'].rsplit('/', 1)[1].rsplit('?', 1)[0]
				# print(f"cur_im {cur_im}")
				if(im == cur_im):
					fout.write(media['caption']+'\n')
					for tag in media["hashtags"]:
						tag_dict[tag.lower()] += 1
					fout.write('------------------------------------\n')
					break
	tag_dict = [(k, tag_dict[k]) for k in tag_dict]
	tag_dict = sorted(tag_dict, key=get_v, reverse=True)
	hashtag_counts[i] = tag_dict
fp.close()

with open('tag_counts_img.json', 'w') as fj:
	json.dump(hashtag_counts, fj, indent=4)