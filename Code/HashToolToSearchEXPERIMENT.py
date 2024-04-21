import re
from glob import glob
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize, sent_tokenize
import hashlib

f = open('TextFiles/frankenstein.txt','r', encoding='latin-1')
s=f.read()
#might be worth adding a .lower somewhere so that imputs are santized to be same
words=word_tokenize(s)


sentences=sent_tokenize(s)#might not be hash


#stores each word in a dictionary with word being key and having multiple values
#whre each value is a location of where that words appears
locations={}
for i, w in enumerate(words):
    if w != '':
        locations.setdefault(w, []).append(i)


#prints out wrods before and after it to print page, might need adjustment
def get_page(word, index, window_size=200):
    start = max(0, index - window_size)
    end = min(len(words), index + window_size + 1)
    context = words[start:end]
    #highlights word using ()
    context[index - start] = f'({word})'#NOT VERY CLEAR consider chaning later

    return context


search_word = 'sailing over'
if search_word in locations:
    print(f"Occurrences of '{search_word}': {len(locations[search_word])}")
    for i,index in enumerate(locations[search_word],start=1):
        # Retrieve and print surrounding words
        print(f"\nExample {i}/{len(locations[search_word])}:\n")
        page = get_page(words[index], index)
        print(' '.join(page))
        if i < len(locations[search_word]):
            choice = input("\nDo you want to see another example? (yes/no): ").lower()
            if choice != 'yes':
                break
else:
    print(f"'{search_word}' not found in the text.")



# sentence seraching but as its not using diconarys might not counts as hash
#

def get_context_sentence(sentence_list, index, window_size=1):
    start = max(0, index - window_size)
    end = min(len(sentence_list), index + window_size + 1)
    context = sentence_list[start:end]
    return context

search_phrase = 'Project Gutenberg'
found = False
for i, sentence in enumerate(sentences):
    if search_phrase in sentence:
        print(f"\nExample {i + 1}:\n")
        # Retrieve and print surrounding sentences
        context = get_context_sentence(sentences, i)
        for j, sent in enumerate(context):
            if search_phrase in sent:
                # Highlight the searched phrase
                sent = sent.replace(search_phrase, f"({search_phrase})")
                print(sent)
        found = True
        break
if not found:
    print(f"'{search_phrase}' not found in the text.")

### Failed attempt below ignore.. using md5 would only allow if the whole
    #sentece matched macking ti worse


# Function to create hash of word or phrase
def get_hash(text):
    return hashlib.md5(text.encode()).hexdigest()

def get_context_sentence(sentence_list, index, window_size=1):
    start = max(0, index - window_size)
    end = min(len(sentence_list), index + window_size + 1)
    context = sentence_list[start:end]
    return context

search_term = input("Enter the search term: ")

search_hash = get_hash(search_term)

hashed_sentences = {}

for i, sentence in enumerate(sentences):
    sentence_hash = get_hash(sentence)
    if search_hash in sentence_hash:
        if sentence_hash not in hashed_sentences:
            hashed_sentences[sentence_hash] = []
        hashed_sentences[sentence_hash].append(i)

if hashed_sentences:
    for hashed_sentence, indices in hashed_sentences.items():
        for index in indices:
            print(f"\nExample {index + 1}:\n")
            # Retrieve and print surrounding sentences
            context = get_context_sentence(sentences, index)
            for j, sent in enumerate(context):
                print(sent)
else:
    print(f"'{search_term}' not found in the text.")

###### Rabin karp search testing so far seems to indicate that it does it perfect
    ## lower case and upper case need ot be kept in mind, more testing needed,
    ## would this count as hash?
def find_sentences_around_index(text, index):
    start_sentence = text.rfind('.', 0, index)
    if start_sentence == -1:
        start_sentence = 0
    else:
        start_sentence += 1

    end_sentence = text.find('.', index)
    if end_sentence == -1:
        end_sentence = len(text)
    else:
        end_sentence += 1

    return text[start_sentence:end_sentence]


def rabin_karp_search(pattern, text):
    # Implementation of Rabin-Karp algorithm for string searching
    d = 256  # Number of characters in the input alphabet
    q = 101  # A prime number
    
    m = len(pattern)
    n = len(text)
    p = 0  # Hash value for pattern
    t = 0  # Hash value for text
    h = 1

    # The value of h would be "pow(d, m-1)%q"
    for i in range(m - 1):
        h = (h * d) % q

    # Calculate the hash value of pattern and first window of text
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q
    matches = 0
    match_indices = []
    # Slide the pattern over text one by one
    for i in range(n - m + 1):
        # Check the hash values of current window of text and pattern
        # If the hash values match, then only check for characters one by one
        if p == t:
            # Check for characters one by one
            for j in range(m):
                if text[i + j] != pattern[j]:
                    break
            j += 1
            # If p == t and pattern[0...m-1] = text[i, i+1, ...i+m-1]
            if j == m:
                matches += 1
                match_indices.append(i)

        # Calculate hash value for next window of text: Remove leading digit,
        # add trailing digit
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            # We might get negative value of t, converting it to positive
            if t < 0:
                t = t + q
    print("Number of matches:", matches)
    
    if matches == 0:
        return
    ## currently doesnt work it jsut prints out the sentece its in twice
    #need to copy over features from other experiments
    for match_index in match_indices:
        print("\nMatch found at index:", match_index)
        print("Sentence before match:", find_sentences_around_index(text, match_index))
        print("Sentence after match:", find_sentences_around_index(text, match_index + m))
        stop = input("Press Enter to see the next match, or type 'q' to quit: ")
        if stop.lower() == 'q':
            break
        
# Example usage
pattern = input("Enter pattern to search: ")
print("Occurrences of the pattern:")
rabin_karp_search(pattern, s)

