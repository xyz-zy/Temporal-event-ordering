import os
import argparse

from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="parse examples from xml")
parser.add_argument('--input_dir', type=str, help="directory containing xml")
parser.add_argument('--out', type=str, help="output filename")
parser.add_argument('--out_dir', type=str, help="output directory")
args = parser.parse_args()

input_folder = args.input_dir
output_folder = args.out_dir

if not input_folder or not output_folder:
  print("please specify args")
  exit()

if not os.path.exists(output_folder):
  os.makedirs(output_folder)

f = open(output_folder + "/" + args.out, "w")
for filename in os.listdir(input_folder):
	full_path = os.path.join(input_folder, filename)
	if not os.path.isfile(full_path) or not filename.endswith("xml"):
		continue
	print(filename)
	soup = BeautifulSoup(open(os.path.join(input_folder, filename)), "html.parser")
	tlinks = [x for x in soup.findAll('tlink')]
	event_pairs = []
	events = []
	for t in tlinks:
		if t.attrs["type"] == "ee" and (t.attrs["origin"] == "TimeTimeSieve" or t.attrs["origin"] == "AdjacentVerbTimex"):
			event_pairs.append((t.attrs["event1"], t.attrs["event2"], t.attrs["relation"]))
			events.append(t.attrs["event1"])
			events.append(t.attrs["event2"])
	event_sent_dict = {}
	for entry in soup.findAll("entry"):
		if str(type(entry)) == "<class 'bs4.element.Tag'>":
			events_entry = {x.attrs["eiid"]: (x.attrs["string"], int(x.attrs['offset'])-1) for x in entry.findAll("event")}
			token_group = entry.find("tokens")
			tokens = []
			for tok in token_group.findAll("t"):
				tok_text = tok.text.replace(" ", "")
				tok_text = tok_text[3:-3]
				tokens.append(tok_text)
			sentence = " ".join(tokens)
			tags = [''] * len(tokens)
			#print(len(tokens))
			for x in entry.findAll("event"):
				tags[int(x.attrs['offset'])-1] = x.attrs['eiid']
			for x in entry.findAll("timex"):
				offset = int(x.attrs['offset'])
				for i in range(int(x.attrs['length'])):
					if offset-1+i >= len(tags):
						print(offset, x.attrs['length'], x.attrs['text'])

					tags[offset-1+i] = x.attrs['tid']
					#print(tokens[offset-1+i])
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
