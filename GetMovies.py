from AwardCounter import AwardCounter

movieDict = AwardCounter()

sampleDict = {}
sampleDict["Coco"] = 1
sampleDict["The Shape of Water"] = 1
sampleDict["Dunkirk"] = 1
sampleDict["The Post"] = 1
sampleDict["Call Me By Your Name"] = 1

sampleTweet1 = "coco is my favorite movie ever"
sampleTweet2 = "i loved the shape of water"
sampleTweet3 = "i thought call by your name was great" # should return false
sampleTweet4 = "i love coco"

def getMovies(sampleTweet, award):
	for i in sampleDict:
		if i.lower() in sampleTweet.lower():
			movieDict.increment(award, i)

# getMovies(sampleTweet1, "Best Drama")
# getMovies(sampleTweet2, "Best Drama")
# getMovies(sampleTweet3, "Best Drama")
# getMovies(sampleTweet4, "Best Drama")
# print movieDict.get_all()

sampleList1 = ["coco", "is", "my", "favorite"]
sampleList2 = ["i", "love", "coco"]
sampleList3 = ["call", "me", "by", "your", "name", "is", "amazing"]

def getMoviesTwo(sampleTweet, award):
	string = ' '.join(sampleTweet)
	for i in sampleDict:
		if i.lower() in string.lower():
			movieDict.increment(award, i)

getMoviesTwo(sampleList1, "Best Movie")
getMoviesTwo(sampleList2, "Best Movie")
getMoviesTwo(sampleList3, "Best Drama")
print movieDict.get_all()
