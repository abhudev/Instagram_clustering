# Plot the distribution of hashtag counts for each cluster of posts


import json
from collections import defaultdict, Counter
import matplotlib.pyplot as plt

# with open('tag_counts_img.json') as fj:
# 	hashtag_counts = json.load(fj)
# with open('tag_counts_likes_img.json') as fj:
# 	hashtag_like_counts = json.load(fj)
# with open('tag_counts_comments_img.json') as fj:
# 	hashtag_comment_counts = json.load(fj)


with open('tag_counts.json') as fj:
	hashtag_counts = json.load(fj)
# with open('tag_counts_likes.json') as fj:
# 	hashtag_like_counts = json.load(fj)
# with open('tag_counts_comments.json') as fj:
# 	hashtag_comment_counts = json.load(fj)

for cur_cat in (hashtag_counts):
	category = hashtag_counts[cur_cat]
	keys = [tup[0] for tup in category]
	counts = [tup[1] for tup in category]
	keys = keys[1:]
	counts = counts[1:]
	point = -1
	for i, val in enumerate(counts):
		if val < 50:
			point = i
			break

	keys = keys[:10]
	counts = counts[:10]

	fig = plt.figure()
	plt.title(f'Category {cur_cat}')
	plt.xlabel('Hashtags')
	plt.ylabel('Counts')
	plt.bar(keys, counts, align='center')
	plt.savefig(f'plots/count_cat_{cur_cat}.png')


# for cur_cat in (hashtag_like_counts):
# 	category = hashtag_like_counts[cur_cat]
# 	keys = [tup[0] for tup in category]
# 	counts = [tup[1] for tup in category]
# 	keys = keys[1:]
# 	counts = counts[1:]
# 	point = -1
# 	for i, val in enumerate(counts):
# 		if val < 50:
# 			point = i
# 			break

# 	keys = keys[:10]
# 	counts = counts[:10]

# 	fig = plt.figure()
# 	plt.title(f'Category {cur_cat}')
# 	plt.xlabel('Hashtags')
# 	plt.ylabel('Counts')
# 	plt.bar(keys, counts, align='center')
# 	plt.savefig(f'plots/count_cat_{cur_cat}_likes.png')


# for cur_cat in (hashtag_comment_counts):
# 	category = hashtag_comment_counts[cur_cat]
# 	keys = [tup[0] for tup in category]
# 	counts = [tup[1] for tup in category]
# 	keys = keys[1:]
# 	counts = counts[1:]
# 	point = -1
# 	for i, val in enumerate(counts):
# 		if val < 50:
# 			point = i
# 			break

# 	keys = keys[:10]
# 	counts = counts[:10]

# 	fig = plt.figure()
# 	plt.title(f'Category {cur_cat}')
# 	plt.xlabel('Hashtags')
# 	plt.ylabel('Counts')
# 	plt.bar(keys, counts, align='center')
# 	plt.savefig(f'plots/count_cat_{cur_cat}_comments.png')