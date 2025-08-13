import glob
import os
import re

pn_questions = "./questions/"


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file: #read file
        content = file.read()
    
    #print(content)
    return content
    
    
    
    #Bunlar bir tuple'a gidecek.
    #Sonra girdiler neler olacak ve ona gore nasil dizecek.
    #Konu keywordleri bir dosya olarak verilmeli
    #Keyword-Difficulty etkilesmesi 1. soru icin adaylar
    #2. soru icin adaylar
    #Sonra radndom olarak adaylardan sec ama aynı soru olmamasına dikkat et
    
    #Ardından hepsini bir dosyada birlestir. Required packageları da dogru diz
    #Latex'le?
    #Bir de bunun icin menu ciksa olur
    
    #Case 2, Sınavın zorlugu: Bu version 2'ye
       
    
#    """ Extract Keywords (comma-separated values after "Keywords: ")"""
#    keywords_match = re.search(r"Keywords:\s*(.*?)\s*END", content, re.DOTALL)
#    if keywords_match:
#        keywords = [k.strip() for k in keywords_match.group(1).split(',')]
#    else:
#        keywords = []

#    # Extract Difficulty (number after "Difficulty: ")
#    difficulty_match = re.search(r"Difficulty:\s*(\d+)", content)
#    difficulty = int(difficulty_match.group(1)) if difficulty_match else None

#    return {
#        "Keywords": keywords,
#        "Difficulty": difficulty
#    }
    
def extract_field(content, field):
    """
    Extracts text between {FIELD: ... END}
    Returns:
        - str: The extracted content (or None if not found).
    """
    pattern = rf"{{{field}:\s*(.*?)\s*END\}}"
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1).strip() if match else None

# Example usage
#result = parse_file("your_file.txt")
#print("Keywords:", result["Keywords"])
#print("Difficulty:", result["Difficulty"])



for qn in sorted(os.listdir(pn_questions)):
   fn=pn_questions+qn
   content=read_file(fn)
   Keywords   = extract_field(content,"Keywords")
   Difficulty = extract_field(content,"Difficulty")





