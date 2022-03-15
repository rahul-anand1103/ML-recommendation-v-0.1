from re import L
import pandas as pd
from tqdm import tqdm
from config import *

class GettingDataCatergory:
    def __init__(self,course_name) -> None:
        self.course_name=course_name
        
    def csv_load(self)->None:
        self.categories=pd.read_csv(MAIN_DATA_PATH+'categories.csv')
        self.learn_contents=pd.read_csv(MAIN_DATA_PATH+'learn_contents.csv')
        self.learn_contents_topics=pd.read_csv(MAIN_DATA_PATH+'learn_contents__topics.csv')
        self.sub_categories=pd.read_csv(MAIN_DATA_PATH+'sub_categories.csv')
        self.topics=pd.read_csv(MAIN_DATA_PATH+'topics.csv')
        self.skills_df=pd.read_csv(MAIN_DATA_PATH+"learn_contents__skills.csv")
        self.skills_names=pd.read_csv(MAIN_DATA_PATH+"skills.csv")
        self.partner_df=pd.read_csv(MAIN_DATA_PATH+"partners.csv")

    def get_category(self)->None:
        self.categories_id=self.categories[self.categories["default_display_label"]==self.course_name]["id"].values[0]
        

    def get_sub_category(self)->None:
        self.sub_catergory_id_list=list(self.sub_categories[self.sub_categories["category"]==self.categories_id]["id"].values)
       

    def topic_sub_category(self)->None:
        topic_id_list=[]
        for sub_id in self.sub_catergory_id_list:
            topic_id_list.append(list(self.topics[self.topics["sub_category"]==sub_id]["id"].values))
        self.topic_id_list=topic_id_list
      

    def get_course_from_content(self)->None:
        learn_content=[]
        for topic_id in self.topic_id_list:
            for id in topic_id:
                learn_content.append(list(self.learn_contents_topics[self.learn_contents_topics["topic_id"]==id]['learn_content_id'].values))
        self.learn_content_id=learn_content
    

    def course_id_to_dataframe(self)->None:
        for index,ids in tqdm(enumerate(self.learn_content_id)):
            if index==0:
                for inside_index,id_ in enumerate(ids):
                    if inside_index==0:
                        self.main_df=self.learn_contents[self.learn_contents["id"]==id_]
                    else:
                        df1_=self.learn_contents[self.learn_contents["id"]==id_]
                        frames = [self.main_df, df1_]
                        self.main_df = pd.concat(frames)
            else:
                for inside_index,id_ in enumerate(ids):
                    df1_=self.learn_contents[self.learn_contents["id"]==id_]
                    frames = [self.main_df, df1_]
                    self.main_df = pd.concat(frames)

    def approved_course(self)->None:
        self.main_df=self.main_df[self.main_df["internal_status"]=="approved"]


    def get_skills_dataframe(self)->None:
        skills_add=[]
        for ids in self.main_df["id"]:
            ids_skill_list=[]
            for skill_id in list(self.skills_df[self.skills_df['learn_content_id']==ids]["skill_id"].values):
                ids_skill_list.append(self.skills_names[self.skills_names["id"]==skill_id]["default_display_label"].values[0])
            skills_add.append(ids_skill_list)
        self.main_df["skills"]=skills_add

    def get_partner_name(self)->None:
        partner_list=[]
        for par in self.main_df["partner"]:
            partner_list.append(self.partner_df[self.partner_df["id"]==int(par)]["name"].values[0])
        self.main_df["partner"]=partner_list
    
    def consider_columns(self):
        consider=["id","title","description","skills","content","partner"]
        self.main_df=self.main_df[consider]
        #print(self.main_df.shape)

    def dataframe_to_csv(self)->None:
        file_name=self.course_name+".csv"
        self.main_df.to_csv(PATH_ORIGINAL+file_name,index=False)


def main():
    for catergory in tqdm(['Finance','Healthcare','Management','Healthcare','Creativity & Design',
                            'Personal Development','Emerging Technologies','Data & Analytics','Science & Social Sciences',
                            'Software & Information Technology','Blockchain','Cloud & Security','Big Data & Data Science',
                            'Engineering','Degree Program']):
        getting_data_catergory=GettingDataCatergory(catergory)
        getting_data_catergory.csv_load()
        getting_data_catergory.get_category()
        getting_data_catergory.get_sub_category()
        getting_data_catergory.topic_sub_category()
        getting_data_catergory.get_course_from_content()
        getting_data_catergory.course_id_to_dataframe()
        getting_data_catergory.approved_course()
        getting_data_catergory.get_skills_dataframe()
        getting_data_catergory.get_partner_name()
        getting_data_catergory.consider_columns()
        getting_data_catergory.dataframe_to_csv()


if __name__ == "__main__":
    main()