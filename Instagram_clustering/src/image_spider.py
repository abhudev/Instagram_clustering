import scrapy
from scrapy.crawler import CrawlerProcess
import os
import logging
import json
import argparse


# img_links - JSON file containing list of image links
# out_dir - directory where images are stored
parser = argparse.ArgumentParser()
parser.add_argument('--img_links')
parser.add_argument('--out_dir')
args = parser.parse_args()

img_links = []

if(args.out_dir is None):
    exit()

with open(args.img_links, 'r') as fin:
    img_json = json.load(fin)
    img_links = img_json["img_links"]

try:
    os.mkdir(args.out_dir)
except:
    pass

# Download IG images
class ImgSpider(scrapy.Spider):
    name = "img"
    
    # Describe requests
    def start_requests(self):        
        for url in img_links:
            req = scrapy.Request(url, self.save_img)
            im_name = url.rsplit('/', 1)[1].rsplit('?', 1)[0]
            p_im = os.path.join(args.out_dir, im_name)
            req.meta["img_path"] = p_im
            yield req   

    # Save images
    # Don't use image libraries 
    # Since some formats may not be recognized
    def save_img(self, response):
        p_im = response.meta["img_path"]
        with open(p_im, "wb") as fout:
            # Body of page is image data
            fout.write(response.body)    
        

# Be polite! Set a download delay, in seconds.
# Reduce/increase concurrent requests if needed
# Set settings and run spider
# TODO - autothrottle
# THings to explore- 
# 1. Autothrottle 2. Pipelines 3. Writing to database 4. Xpath 5. Infinite scrolling
img_settings = {
                    "BOT_NAME": 'igimg',
                    "LOG_LEVEL": "WARNING",
                    "USER_AGENT": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
                    "ROBOTSTXT_OBEY": True,
                    "CONCURRENT_REQUESTS": 32,
                    "DOWNLOAD_DELAY": 1.5
                }                

img_process = CrawlerProcess(settings=img_settings)
img_process.crawl(ImgSpider)
img_process.start(stop_after_crawl=False)