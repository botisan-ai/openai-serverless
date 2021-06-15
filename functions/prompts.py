def extract_people_names_prompt(message):
    return f'''
Extract the people names from the message. Put one name per line.

Message:
I am actually the assistant here with Justin Hahn so I'm here to answer any questions you might have!
People names:
Justin Hahn
####
Message:
My name is Raiya and I work for Karie Milford at Milford Real Estate.
People names:
Raiya
Karie Milford
####
Message:
I will pass this on to my associate, Shane Hamilton, right away and let them coordinate a time with you
People names:
Shane Hamilton
####
Message:
Hugo Avalos will be in touch with you at (323) 548-1370
People names:
Hugo Avalos
####
Message:
{message}
People names:
'''.strip()

def split_sentences_prompt(sentence):
    return f'''
Split the message into individual sentences. Put each sentence into its own line. Keep the original punctuations as much as possible.

Message:
Hi, my name is Simon. I am working on a sentence splitter powered by OpenAI
Sentences:
Hi, my name is Simon.
I am working on a sentence splitter powered by OpenAI
####
Message:
{sentence}
Sentences:
'''.strip()

def extract_todo_list_prompt(sentence):
    return f'''
Given a message, figure out the person's to-do list.

Message:
I have a meeting tomorrow at 10am, then I want to go to the gym for a swim before finishing the videos.
To-do List:
[{{"item":"meeting","time":"10am"}},{{"item":"swim at gym"}},{{"item":"finish the videos"}}]
####
Message:
I have a zoom call at 11am, then I need to finish writing the code for demo.
To-do List:
[{{"item":"zoom call","time":"11am"}},{{"item":"finish writing the code for demo"}}]
####
Message:
I need to go to the gym in the morning at 10am, then I am driving to the hotel and check-in in the afternoon. At night I need to finish preparing for the video shooting.
To-do List:
[{{"item":"go to the gym","time":"10am"}},{{"item":"drive to the hotel and check-in","time":"afternoon"}},{{"item":"finish preparing for the video shooting","time":"night"}}]
####
Message:
I need to pack our car, and then get our car washed, before we hit the road.
To-do List:
[{{"item":"pack our car"}},{{"item":"get our car washed"}},{{"item":"hit the road"}}]
####
Message:
I have zoom calls at 10am and 2pm, and I need to finish the message parsing.
To-do List:
[{{"item":"zoom call","time":"10am"}},{{"item":"zoom call","time":"2pm"}},{{"item":"finish the message parsing"}}]
####
Message:
I want to finish the video by Friday, and do some shopping on Saturday.
To-do List:
[{{"item":"finish the video","time":"Friday"}},{{"item":"do some shopping","time":"Saturday"}}]
Message:
{sentence}
To-do List:
'''.strip()
