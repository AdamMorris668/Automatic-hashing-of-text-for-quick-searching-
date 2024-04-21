import os
#Checks folder for all text files and returns what options suer has
def list_text_files(directory):
    text_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    return text_files

def select_file(files):
    print("Available text files:")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")
    
    while True:
        try:
            choice = int(input("Enter the number of the file you want to select: "))
            if 1 <= choice <= len(files):
                return files[choice - 1]
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

#Finds set amount of words surroding the searched term
def find_paragraphs_around_index(text, index):
    start_paragraph = text.rfind('.', 0, index)
    if start_paragraph == -1:
        start_paragraph = 0
    else:
        start_paragraph = text.find('\n', start_paragraph) + 1
    
    end_paragraph = text.find('.', index)
    if end_paragraph == -1:
        end_paragraph = len(text)
    else:
        end_paragraph = text.find('\n', end_paragraph)
    
    context_start = max(0, start_paragraph - 200)
    context_end = min(len(text), end_paragraph + 200)
    
    return text[context_start:context_end].strip()

#surronds the searched word, since cant use HTML to highlight in python shell
def highlight_word(text, pattern):
    return text.replace(pattern, " ||{}|| ".format(pattern))

#Robin karp algorithm
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
            #If negative value of t, converting it to positive
            if t < 0:
                t = t + q
    print("Number of matches:", matches)
    
    if matches == 0:
        return
    
    #Prints out surroding text of the searched term 
    
    for match_index in match_indices:
        print("\nMatch found at index:", match_index)
        
        context = find_paragraphs_around_index(text, match_index)
        highlighted_context = highlight_word(context, pattern)
        
        print("Surrounding paragraphs containing the match:")
        print(highlighted_context)
        
        stop = input("Press Enter to see the next match, or type 'q' to quit: ")
        if stop.lower() == 'q':
            break

        
#List  text files in folder and let the user select one
directory = 'TextFiles'
text_files = list_text_files(directory)
selected_file = select_file(text_files)

#Read the selected text file
with open(os.path.join(directory, selected_file), 'r', encoding='latin-1') as file:
    s = file.read()

#User pattern input and running the search
pattern = input("Enter pattern to search: ")
print(f"Occurrences of the pattern in {selected_file}:")
rabin_karp_search(pattern, s)

