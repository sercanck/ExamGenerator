import glob
import os
import re
import random


pn_questions  = "./questions/"  #Name of the question folder
template_name = "template.tex"  #Name of the exam's template
output_name   = "exam.tex"      #Name of the exam

question_list = []  
packages_list = dict()
questions_all = ""        
packages_all  = ""

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file: #read file
        content = file.read()
    file.close()
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

def extract_packages(content,plist):
    """
    Extract text between {Requiredpackages: ... END}
    Parse command and argument part seperately
    command= usepackages, tikzlibrary... etc.
    arguments= tikz,... etc.
    plist =  package list
    """
    content_temp=extract_field(content, "Requiredpackages")
    for line in content_temp.splitlines():
      command, arguments = line.split(": ")

    #TODO: Requiredpackage yoksa...


    if command in list(packages_list.keys()): #If the command exists
      for package in arguments.split(","):
        if package not in plist[command]:
          plist[command] = plist[command]+","+package
    else:
      plist[command]=arguments

    return plist


with open('exam_structure','r') as file_structure:
    for line in file_structure.readlines(): #Loop over target question
      question, target_keyword, target_difficulty = line.rstrip("\n").split(": ")
      possible_questions = []

      """Find suitable questions"""
      for qn in sorted(os.listdir(pn_questions)):
        if qn in question_list: #If this question is already selected.
          continue
      
        fn=pn_questions+qn
        content=read_file(fn)
        Keywords   = extract_field(content,"Keywords")
        Difficulty = extract_field(content,"Difficulty")
 
        #TODO:Tüm dosyaları okumak zahmetli grep gibi bir sey olsa iyi is gorurdu
        
        if (target_difficulty==Difficulty) and (target_keyword in Keywords):           
          possible_questions.append(qn)
          #TODO: target_keyword birden fazla olabilir           

      if not possible_questions: 
        print("Cannot find a suitable question candidate for "+question+"!!!")  #if possible_questions is empty do something...
      else:  
        question_list.append(random.choice(possible_questions))      
                  

"""Merge questions and packages"""        
for qn in question_list:
  
  fn=pn_questions+qn
  content=read_file(fn)
  text = extract_field(content,"Text")
  questions_all += text + "\n" + "\n"   

  packages_list = extract_packages(content,packages_list)


for cmd in list(packages_list.keys()): #for each command
  packages_all = packages_all+"\\"+cmd+"{"+packages_list[cmd]+"}"+"\n"  #write and next line


 
"""Read template and replace Questions and packages""" 
with open(template_name, 'r', encoding='utf-8') as file: #read file
     content_template = file.read()


content_template=content_template.replace("QUESTIONSHERE",questions_all)     
content_template=content_template.replace("PACKAGESHERE",packages_all)     


with open(output_name,'w') as file: #read file
     file.write(content_template)


          
        






