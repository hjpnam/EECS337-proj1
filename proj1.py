import textblob as tb
import json
import os
import re

data = json.load(open('gg2018.json'))

for i in range(100):
	
gi	print re.search(data[i]['text'], "bestdirector", flags=re.I)