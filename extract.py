import json


def dataextraction():
    with open("structTweets.json", "r", encoding="utf-8") as readfile:
        data = json.load(readfile)

    try:

        wtt = open("Tweets_extracted.txt", "w+")
        wtt.flush()
        count = -1
        da = []
        for line in data:

            count += 1
#			print(data)
#		if(data[line]["lang"] == "en"):
            print(line["created_at"], count)
            if(line.get("retweeted_status")):
                if(line["retweeted_status"].get("extended_tweet")):
                    wtt.write(line["retweeted_status"]["extended_tweet"]
                              ["full_text"].replace("\n", " "))
                    wtt.write("\n")
                else:
                    wtt.write(line["retweeted_status"]
                              ["text"].replace("\n", " "))
                    wtt.write("\n")
#					wtt.write("\n")
            elif (line.get("extended_tweet")):
                if(line["extended_tweet"].get("full_text")):
                    wtt.write(line["extended_tweet"]
                              ["full_text"].replace("\n", " "))
                    wtt.write("\n")
#					wtt.write("\n")
            else:
                if(line.get("text")):
                    wtt.write(line["text"].replace("\n", " "))
                    wtt.write("\n")
#					wtt.write("\n")

    finally:
        wtt.close()


# dataextraction()
