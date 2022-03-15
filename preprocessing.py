from config import *
import numpy as np
import pandas as pd
from tqdm import tqdm
import re
import ast
import nltk

#nltk.download('punkt')
#nltk.download('stopwords')

class preprocessing:
    def __init__(self,category_name) -> None:
        self.category_name=category_name
    
    def read_csv_preprocessing(self)->None:
        file_name=self.category_name.lower()+".csv"
        self.data_csv=pd.read_csv(PATH_ORIGINAL+file_name)
    
    def cleanhtml(self,text):
        CLEANR = re.compile('<.*?>') 
        return re.sub(CLEANR, ' ',text)

    def cleanbracket(self,text):
        return re.sub(r"\([^()]*\)", "", text)
    
    def remove_duplicate(self):
        self.data_csv=self.data_csv.drop_duplicates(subset=['id'], keep='last')


    def text_expansion(self,text):
        text = re.sub(r"i'm", "i am", text)
        text = re.sub(r"he's", "he is", text)
        text = re.sub(r"she's", "she is", text)
        text = re.sub(r"that's", "that is", text)        
        text = re.sub(r"what's", "what is", text)
        text = re.sub(r"where's", "where is", text) 
        text = re.sub(r"\'ll", " will", text)  
        text = re.sub(r"\'ve", " have", text)  
        text = re.sub(r"\'re", " are", text)
        text = re.sub(r"\'d", " would", text)
        text = re.sub(r"\'ve", " have", text)
        text = re.sub(r"won't", "will not", text)
        text = re.sub(r"don't", "do not", text)
        text = re.sub(r"did't", "did not", text)
        text = re.sub(r"can't", "can not", text)
        text = re.sub(r"it's", "it is", text)
        text = re.sub(r"couldn't", "could not", text)
        text = re.sub(r"have't", "have not", text)
        text = re.sub(r"[,.\"\'!@#$%^&*(){}?/;`~:<>+=-]", "", text)
        return text
    
    def fun_preprocessing_title(self,title):
        title=title.lower()
        title=self.cleanhtml(title)
        title=self.cleanbracket(title)
        title=self.text_expansion(title)
        title= re.sub('[^A-Za-z0-9]+', ' ', title)
        title=re.sub("\s+" , " ", title)
        return title

    def fun_preprocessing_description(self,description):
        description=description.lower()
        description=self.cleanhtml(description)
        description=self.cleanbracket(description)
        description=self.text_expansion(description)
        description= re.sub('[^A-Za-z0-9]+', ' ', description)
        description=re.sub("\s+" , " ", description)
        return description
    
    def fun_preprocessing_content(self,content):
        content=content.replace("<br>"," ")
        content=self.cleanhtml(content)
        content=content.lower()
        content=re.sub('module [0-9]+:', ' ', content)
        content=re.sub('lecture [0-9]+:', ' ', content)
        content=re.sub('[0-9]+.', ' ', content)
        content=self.text_expansion(content)
        content=content.strip()
        content= re.sub('[^A-Za-z]+', ' ', content)
        content=re.sub("\s+" , " ", content)
        content=self.cleanhtml(content)
        return content

    def removing_space_in_skils(self,L):
        return_text=[]
        for i in L:
            i=i.lower()
            return_text.append(i.replace(" ",""))
        return " ".join(return_text)

    def preprocessing_title(self):
        preprocessing_title_list=[]
        for title in tqdm(self.data_csv["title"]):
            preprocessing_title_list.append(self.fun_preprocessing_title(title))
        self.data_csv['title']=preprocessing_title_list

    def preprocessing_description(self):
        preprocessing_description_list=[]
        for description in tqdm(self.data_csv["description"]):
            preprocessing_description_list.append(self.fun_preprocessing_description(description))
        self.data_csv['description']=preprocessing_description_list
    
    def preprocessing_content(self):
        preprocessing_content_list=[]
        for index,content in tqdm(enumerate(self.data_csv["content"])):
            if type(content)==str:
                content=self.fun_preprocessing_content(content)
                preprocessing_content_list.append(content)
            else:
                preprocessing_content_list.append(" ")
        self.data_csv['content']=preprocessing_content_list
    
    def preprocessing_skills(self):
        preprocessing_skills_list=[]
        for skils in self.data_csv["skills"]:
            preprocessing_skills_list.append(self.removing_space_in_skils(ast.literal_eval(skils)))
        self.data_csv['skills']=preprocessing_skills_list
    
    def dataframe_to_csv(self)->None:
        file_name="preprocessing_"+self.category_name+".csv"
        self.data_csv.to_csv(PATH_PREPROCESSED+file_name,index=False)

def main():
    for catergory in tqdm(['Finance','Healthcare','Management','Creativity & Design',
                            'Personal Development','Emerging Technologies','Data & Analytics','Science & Social Sciences',
                            'Software & Information Technology','Blockchain','Cloud & Security','Big Data & Data Science',
                            'Engineering','Degree Program']):
        preprocessing_obj=preprocessing(catergory)
        preprocessing_obj.read_csv_preprocessing()
        preprocessing_obj.preprocessing_title()
        preprocessing_obj.preprocessing_description()
        preprocessing_obj.preprocessing_content()
        preprocessing_obj.preprocessing_skills()
        preprocessing_obj.remove_duplicate()
        preprocessing_obj.dataframe_to_csv()

if __name__ == "__main__":
    main()