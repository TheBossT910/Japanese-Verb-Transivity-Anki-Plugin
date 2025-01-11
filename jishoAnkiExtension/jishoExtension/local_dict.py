# Monday June 3 2024
# Local dictionary testing instead of web scraper
# Taha Rashid

from jamdict import Jamdict
import asyncio
import re
#import time


async def search(kanji, kana, write):
    jam = Jamdict()  #memory mode does not work :(
    # kanji = "食べる"
    # kana = "たべる"
    ans = ""
    write_no_case = str(write).lower()

    #run the dictionary if it is a verb and it has NOT been scrapped before
    if (write_no_case.find("verb") != -1) and not ((write_no_case.find("move") != -1)):
        query = kana + " (" + kanji + ")"
        #print(query)
        result = jam.lookup_iter(kanji)

        # print all word entries
        for entry in result.entries:
            #empty = True
            saved = re.split(r"\d\. ", str(entry))
            if len(saved) >= 2:
                # find the correct string
                if (saved[0].find(query) != -1):
                    # check for transivity
                    if (saved[1].find("|transitive") != -1):
                        ans += "Self-Move, "
                        #empty = False
                    if (saved[1].find("|intransitive") != -1):
                        ans += "Other-Move, "
                        #empty = False
                    # if (empty):
                    #     ans = "Not applicable...."

                    # exit
                    ans = ans.rstrip(", ")
    #             else:
    #                 ans = "No matching verb definition"
    #         else:
    #             ans = "No valid definition found (at all)"
    #     if len(ans) <= 0:
    #         ans = "No entries in dictionary"
    # else:
    #     ans = "Already done, or not a verb!"
    return ans


async def run(pairs):
    results = await asyncio.gather(
        *[search(kanji, kana, write) for kanji, kana, write in pairs],
        return_exceptions=True
    )
    return results


#DEBUG
# running the function
# pairs = [("食べる", "たべる"), ("開く", "ひらく"), ("回す", "まわす"), ("開く", "あく")]
# #pairs = [("開く", "あく")]
#
# start_time = time.time()  # timing code...
# results = asyncio.run(run(pairs))
# end_time = time.time()
# execution_time = end_time - start_time
# print(str(execution_time))
#
# print(results)
# temp = "[id#1586270] あく (開く) : 1. to open (e.g. doors) ((Godan verb with 'ku' ending|intransitive verb)) 2. to open (e.g. business, etc.) ((Godan verb with 'ku' ending|intransitive verb)) 3. to be empty ((Godan verb with 'ku' ending|intransitive verb)) 4. to be vacant/to be available/to be free ((Godan verb with 'ku' ending|intransitive verb)) 5. to be open (e.g. neckline, etc.) ((Godan verb with 'ku' ending|intransitive verb)) 6. to have been opened (of one's eyes, mouth, etc.) ((Godan verb with 'ku' ending|intransitive verb)) 7. to come to an end ((Godan verb with 'ku' ending|intransitive verb)) 8. to open (one's eyes, mouth, etc.) ((Godan verb with 'ku' ending|transitive verb)) 9. to have a hole/to form a gap/to have an interval (between events) ((Godan verb with 'ku' ending|intransitive verb))"

# [id#1358280] たべる (食べる) : 1. to eat ((Ichidan verb|transitive verb)) 2. to live on (e.g. a salary)/to live off/to subsist on
