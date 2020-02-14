import gzip
import os
import re

from bs4 import BeautifulSoup

DATA_PATH = "../../../gigaword_eng_5/data/"
folders = ["nyt_eng"] 
OUTPUT_PATH = "./data_processed/"

if not os.path.exists(OUTPUT_PATH):
	os.mkdir(OUTPUT_PATH)

for folder in folders:
	if not os.path.exists(OUTPUT_PATH + folder):
		os.mkdir(OUTPUT_PATH + folder)
	for filename in os.listdir(DATA_PATH + folder):
		print(filename)
		OUT_DIR = os.path.join(OUTPUT_PATH, folder, filename[:-3])
		if not os.path.exists(OUT_DIR):
			os.mkdir(OUT_DIR)
		file = gzip.open(os.path.join(DATA_PATH + folder, filename))
		soup = BeautifulSoup(file, "html.parser")
		for doc in soup("doc"):
			docname = doc.attrs['id']
			print(docname)
			paragraphs = []
			for p in doc("p"):
				para = p.get_text().strip()
				para = re.sub(r"\n+", "\n", para)
				para = para.replace("\n", " ")
				paragraphs.append(para)
			final = " ".join(paragraphs)
			if final.strip() == "":
				continue 
			f = open(os.path.join(OUTPUT_PATH, folder, filename[:-3], docname), "w")
			f.write(final)
			f.close()
