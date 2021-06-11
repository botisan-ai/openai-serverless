def extract_people_names_prompt(message):
    return f'''
Extract the people names from the message. Put one name per line.
####
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
####
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
