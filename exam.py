import glob
import os
import re
import random
import numpy as np
import shutil


#TODO: Tüm dosyaları okumak zahmetli grep gibi bir sey olsa iyi is gorurdu ama yok.
#TODO: Cevap anahtarı
#TODO: Windows/Linux farkı pathler icin

"""
iscopy_figures:
  True: Create a folder named as figure_folder. Copy figures from pn_question/figure_database to figure_folder.
        Rename figure names in the questions as figure_name -> figure_folder/figure_name
        
  False: The code does not do anything related with figures. So, figure names should be written in the question database
         as pn_questions/figures/figure_name ". By that way, output Latex file can be compiled without errors.       
"""
iscopy_figures=True        




target_overall_difficulty = 4


if target_overall_difficulty>0:
  mode=2
else:
  mode=1

sigma=5.0    #Sigma of the Gaussian distrubition used in the 2nd mode

pn_questions    = "./questions/"  #Name of the question database folder
template_name   = "template.tex"  #Name of the exam's template
output_name     = "exam.tex"      #Name of the exam
figure_database = "figures"       #Name of the figure database folder 
figure_folder   = "figures_exam"  #Name of the figures folder which will be created by this code

question_list   = []   
question_dict = dict()   #Required for the 2nd mode
difficulty_dict = dict() #Required for the 2nd mode
packages_dict = dict()
questions_all = ""        
packages_all  = ""
figure_names  = []



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
    
    if not bool(re.search(r'[a-zA-Z]', content_temp)): #If there is not any Requiredpackage...
      return plist   #Do nothing

    for line in content_temp.splitlines():
      command, arguments = line.split(": ")


    if command in list(plist.keys()): #If the command exists
      for package in arguments.split(","):
        if package not in plist[command]:
          plist[command] = plist[command]+","+package
    else:
      plist[command]=arguments

    return plist

def extract_fignames(content,fglist):
    
    """
      Extract text between {} after each \includegraphic.
      Figure names should be on the same line with \includegraphic
      Append them to the fglist
    """
    pattern = r"\\includegraphics.*\{(.*?)\}"
    matches=re.findall(pattern, content)
    for fg_name in matches:
      fglist.append(fg_name)
    return

def copy_figures(fglist):
   for fg in fglist:
     pn_from=os.path.join(pn_questions,figure_database,fg)
     pn_to=os.path.join(figure_folder,fg)
   shutil.copy(pn_from, pn_to)     
     

if not os.path.isdir(figure_folder): #if figure_folder not exist:
  os.mkdir(figure_folder)            #makedir figure_folder



if len(os.listdir(figure_folder))>0:  # if figure_folder not empty:
   isclean=input("Figure folder is not empty. Would you like to clean? (Y/N): ")
   if isclean=="Y":
     for file_name in os.listdir(figure_folder):
       os.remove(os.path.join(figure_folder,file_name))
     


if mode==1: #Questions are selected based on individual difficulty       

  print("Questions will be selected based on individual difficulties.")
  with open('exam_structure','r') as file_structure:
    for line in file_structure.readlines(): #Loop over target question
      question, target_keyword, target_difficulty = line.rstrip("\n").split(": ")
      possible_questions = []

      """Find suitable questions"""
      for qn in sorted(os.listdir(pn_questions)):
        if qn in question_list: #If this question is already selected, skip
          continue
          
        fn=pn_questions+qn

        if not os.path.isfile(fn): #If it is a folder, skip
          continue
      
        content=read_file(fn)
        Keywords   = extract_field(content,"Keywords")
        Difficulty = extract_field(content,"Difficulty")
    
        if "," in target_keyword: #If target keyword is plural
          if (target_difficulty==Difficulty) and set(target_keyword.split(",")).issubset(set(Keywords.split(", "))) :
            possible_questions.append(qn) 
        else: #If target keyword is singular
          if (target_difficulty==Difficulty) and (target_keyword in Keywords):           
            possible_questions.append(qn)

      if possible_questions: 
        question_list.append(random.choice(possible_questions))      
      else:  
        print("Cannot find a suitable question candidate for "+question+"!!!")  #if possible_questions is empty do something...

  """Merge questions and packages"""        
  for qn in question_list:
  
    fn=pn_questions+qn
    content=read_file(fn)
    text = extract_field(content,"Text")

    if bool(re.search(r"\\includegraphics",text)): 
      extract_fignames(text,figure_names)

    questions_all += text + "\n" + "\n"   

    packages_dict = extract_packages(content,packages_dict)

  for cmd in list(packages_dict.keys()): #for each command
    packages_all = packages_all+"\\"+cmd+"{"+packages_dict[cmd]+"}"+"\n"  #write and next line
    
 
  """Read template and replace Questions and packages""" 
  with open(template_name, 'r', encoding='utf-8') as file: #read file
     content_template = file.read()


  content_template=content_template.replace("QUESTIONSHERE",questions_all)     
  content_template=content_template.replace("PACKAGESHERE",packages_all)     


  with open(output_name,'w') as file: #write file
     file.write(content_template)
 
  copy_figures(figure_names)
 
##########################################################
elif mode==2: #Questions are selected based on overall difficulty
  print("Questions will be selected based on overall difficulty ("+str(target_overall_difficulty)+")")
  with open('exam_structure','r') as file_structure:
    possible_questions       = {} #it is a dictionary
    possible_difficulties    = {} #it is a dictionary    
    
    for line in file_structure.readlines(): #Loop over target question
   
      question, target_keyword, target_difficulty = line.rstrip("\n").split(": ")

      possible_questions.setdefault(question, [])      #create a key in dict
      possible_difficulties.setdefault(question, [])   #create a key in dict
      question_dict.setdefault(question, [])   #create a key in dict
      difficulty_dict.setdefault(question, [])   #create a key in dict      
       
      """Find suitable questions"""
      for qn in sorted(os.listdir(pn_questions)):
   
        fn=pn_questions+qn
 
        if not os.path.isfile(fn): #If it is a folder.
          continue
     
        content=read_file(fn)
        Keywords   = extract_field(content,"Keywords")
        Difficulty = extract_field(content,"Difficulty")
    
        if "," in target_keyword: #If target keyword is plural
          if set(target_keyword.split(",")).issubset(set(Keywords.split(", "))) : 
            possible_questions[question].append(qn)
            possible_difficulties[question].append(Difficulty)
        else: #If target keyword is singular
          if target_keyword in Keywords:           
            possible_questions[question].append(qn)
            possible_difficulties[question].append(Difficulty)

  sorted_possible_questions = sorted(possible_questions.items(), key=lambda item: len(item[1]))
      
            
  current_overall_difficulty = 0
  selected_question          = 0

  for question, possible_q_list in sorted_possible_questions:

    if possible_q_list: #There are canditates
      target_difficulty= target_overall_difficulty*(selected_question+1) - current_overall_difficulty*selected_question 
      possible_d_list = np.array(possible_difficulties[question],dtype=float)
      #Eger coktan secilmisses prob 0 olmalı      
            
            
      d_prop = np.exp(-(possible_d_list-target_difficulty)**2/sigma) 
      d_prop = d_prop/sum(d_prop)  #Normaliaze to 1

      index_q = int( np.random.choice(np.arange(0,len(possible_d_list),1,dtype=int),1,p=d_prop))      #Select the index of the question
      
      question_dict[question] = possible_q_list[index_q]
      difficulty_dict[question] = possible_d_list[index_q]
      
      current_overall_difficulty = ( current_overall_difficulty*selected_question + possible_d_list[index_q] ) / (selected_question+1)
      selected_question +=1
    else:
      print("Cannot find a suitable question candidate for "+question+"!!!")  #if possible_questions is empty do something...

  print("##############")      
  print("Overall difficulty of the exam: "+str(current_overall_difficulty))    
      
  """Merge questions and packages"""        
  for qn in question_dict.values():
    if qn:
      fn=pn_questions+qn
      content=read_file(fn)
      text = extract_field(content,"Text")
      questions_all += text + "\n" + "\n"   

      if bool(re.search(r"\\includegraphics",text)): 
        extract_fignames(text,figure_names)
          
      packages_dict = extract_packages(content,packages_dict)


  for cmd in list(packages_dict.keys()): #for each command
    packages_all = packages_all+"\\"+cmd+"{"+packages_dict[cmd]+"}"+"\n"  #write and next line

 
  """Read template and replace Questions and packages""" 
  with open(template_name, 'r', encoding='utf-8') as file: #read file
     content_template = file.read()


  content_template=content_template.replace("QUESTIONSHERE",questions_all)     
  content_template=content_template.replace("PACKAGESHERE",packages_all)     


  with open(output_name,'w') as file: #write file
     file.write(content_template)
 
  copy_figures(figure_names)
  
  with open('exam.log','w') as file:
    file.write("Question  Difficulty\n\n")
    for question, difficulty in difficulty_dict.items():
       print(question+'  '+str(difficulty))
       file.write(question+8*' '+str(difficulty)+'\n')





