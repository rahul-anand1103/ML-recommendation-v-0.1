from config import *
import os
import pandas as pd

def combine_sim_matrix():
    similairy_all = os.listdir(PATH_MATRIX)
    datafame_name=[]
    for sim in similairy_all:
        datafame_name.append(pd.read_csv(PATH_MATRIX+sim))
    frames = datafame_name
    result = pd.concat(frames)
    result.to_csv(PATH_MATRIX+"final_sim_matrix.csv",index=False)


def main():
    combine_sim_matrix()

if __name__ == "__main__":
    main()

