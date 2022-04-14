import csv
import random

VIDEOS = []
with open("list.csv", "r", encoding="utf-8") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    VIDEOS += [(title, url_id) for title, url_id in spamreader]
random.shuffle(VIDEOS)
