import os
import argparse

from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="parse examples from xml")
parser.add_argument('--input_dir', type=str, help="directory containing xml")
parser.add_argument('--out', type=str, help="output filename")
args = parser.parse_args()

input_folder = args.input_dir

f = open("extracted/" + args.out, "w")
for filename in os.listdir(input_folder):
	print(filename)
	soup = BeautifulSoup(open(os.path.join(input_folder, filename)), "html.parser")
	tlinks = [x for x in soup.findAll('tlink')]
	event_pairs = []
	events = []
	for t in tlinks:
		if t.attrs["type"] == "ee":
			event_pairs.append((t.attrs["event1"], t.attrs["event2"], t.attrs["relation"]))
			events.append(t.attrs["event1"])
			events.append(t.attrs["event2"])
	event_sent_dict = {}
	for entry in soup.findAll("entry"):
		if str(type(entry)) == "<class 'bs4.element.Tag'>":
			events_entry = {x.attrs["eiid"]: (x.attrs["string"], int(x.attrs['offset'])-1) for x in entry.findAll("event")}
			sentence = entry.find("sentence").text
			tags = [''] * len(sentence.split())
			for x in entry.findAll("event"):
				tags[int(x.attrs['offset'])-1] = x.attrs['eiid']
			for x in entry.findAll("timex"):
				for i in range(int(x.attrs['length'])):
					tags[int(x.attrs['offset'])-1+i] = x.attrs['tid']
			event_list = set(events).intersection(set(events_entry.keys()))
			if len(event_list) > 0:
				for e in event_list:
					event_sent_dict[e] = (events_entry[e][0], sentence, events_entry[e][1], tags)
	for e1, e2, r in event_pairs:
		f.write("%s  %s  %s\n" % (event_sent_dict[e1][0], r,  event_sent_dict[e2][0]))
		f.write("%s  %s\n" % (event_sent_dict[e1][2], event_sent_dict[e2][2]))
		f.write("%s \n" % event_sent_dict[e1][1])
		f.write(",".join(event_sent_dict[e1][3])+"\n")
		f.write("%s \n" % event_sent_dict[e2][1])
		f.write(",".join(event_sent_dict[e2][3])+"\n")
		f.write(filename)
		f.write("\n")
		f.write("\n")
