import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
from config import *

class SimilarityMatrixModel:
    def __init__(self,category_name) -> None:
        self.category_name=category_name
    
    def read_csv_preprocessing(self)->None:
        file_name="preprocessing_"+self.category_name+".csv"
        self.data_csv=pd.read_csv(PATH_PREPROCESSED+file_name)
        self.learn_contents=pd.read_csv(MAIN_DATA_PATH+'learn_contents.csv')
        self.learn_contents=self.learn_contents[self.learn_contents["internal_status"]=="approved"]
    
    def fillnan(self)->None:
        self.data_csv['title'] = self.data_csv['title'].fillna(" ")
        self.data_csv['description'] = self.data_csv['description'].fillna(" ")
        self.data_csv['skills'] = self.data_csv['skills'].fillna(" ")
        self.data_csv['content'] = self.data_csv['content'].fillna(" ")
        self.data_csv['partner'] = self.data_csv['partner'].fillna(" ")
    
    def main_dataframe(self)->None:
        self.data_csv['tag']=self.data_csv['title']+" "+self.data_csv['description']+" "+self.data_csv['skills']+" "+self.data_csv['content']+" "+self.data_csv['partner']
        self.main=self.data_csv[["id","tag"]]
    
    def model_train(self)->None:
        ifidf=TfidfVectorizer(stop_words='english')
        vector = ifidf.fit_transform(self.main['tag']).toarray()
        self.similarity = cosine_similarity(vector)
    
    def matrix_dataframe(self):
        whole_index=list(self.learn_contents.id)
        main_ids=list(self.main.id)
        x={"id":['']}
        for who_index in whole_index:
            data={who_index:['']}
            x.update(data)
        
        y={"id":['']}
        for new in main_ids:
            data1={new:['']}
            y.update(data1)
        
        df1=pd.DataFrame(x)
        print(df1.shape)
        for index,_ in tqdm(enumerate(self.similarity)):
            df2=pd.DataFrame(y)
            df2.drop(['id'], axis=1,inplace=True)
            df2.iloc[0]=self.similarity[index]
            df1=df1.append(df2, ignore_index = True)
            del df2 
        
        df1.drop(df1.iloc[0].name,inplace=True)
        print(df1.shape)
        print(len(list(df1.columns.values)))
        print(len(main_ids))
        for val in list(df1.columns.values):
            df1[val]=df1[val].fillna(0)
        
        df1["id"]=main_ids
        df1.to_csv(PATH_MATRIX+self.category_name+"_sim_matrix.csv",index=False)
        

def main():
    for catergory in tqdm(['Finance','Healthcare','Management','Creativity & Design',
                            'Personal Development','Emerging Technologies','Data & Analytics','Science & Social Sciences',
                            'Software & Information Technology','Blockchain','Cloud & Security','Big Data & Data Science',
                            'Engineering']):
        model=SimilarityMatrixModel(catergory)
        model.read_csv_preprocessing()
        model.fillnan()
        model.main_dataframe()
        model.model_train()
        model.matrix_dataframe()

if __name__ == "__main__":
    main()