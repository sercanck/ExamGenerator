import glob
import os
import re
import random


pn_questions  = "./questions/"
template_name = "template.tex"
question_list = []


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file: #read file
        content = file.read()
    file.close()
    #print(content)
    return content
    
    
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

with open('exam_structure','r') as file_structure:
    for line in file_structure.readlines(): #Loop over target question
      question, target_keyword, target_difficulty = line.rstrip("\n").split(": ")
      possible_questions = []

      """Find suitable questions"""
      for qn in sorted(os.listdir(pn_questions)):
        if qn in question_list:
          continue
      
        fn=pn_questions+qn
        content=read_file(fn)
        Keywords   = extract_field(content,"Keywords")
        Difficulty = extract_field(content,"Difficulty")
 
        #Tüm dosyaları okumak zahmetli grep gibi bir sey olsa iyi is gorurdu
        
        if (target_difficulty==Difficulty) and (target_keyword in Keywords):           
          possible_questions.append(qn)
          #TODO: target_keyword birden fazla olabilir

      #TODO: if possible_questions is empty do something...
        
      question_list.append(random.choice(possible_questions))   

                  
  
questions_all = ""        
#Loop tex birleştir        
for qn in question_list:
  fn=pn_questions+qn
  content=read_file(fn)
  text = extract_field(content,"Text")
  questions_all += text + "\n" + "\n"   

  #TOD0: Replace packages with usepackage{} and tikzpackage etc.
 
 
with open(template_name, 'r', encoding='utf-8') as file: #read file
     content_template = file.read()


content_template=content_template.replace("QUESTIONSHERE",questions_all)     
print(content_template)
#TODO: write to a new file

          
        






