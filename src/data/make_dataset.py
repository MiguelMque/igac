import pandas as pd

def leer_csv_fr(data_path):
    df=pd.read_csv(data_path+"webscrapping_fr.csv")
    return df


def leer_csv_datosigac(data_path):
    df=pd.read_csv(data_path+'/AvaluoCatastral_JULIO312020.csv',sep=";")
    df2=pd.read_csv(data_path+'/TOTAL_NACIONAL_REG1.txt',sep="\t",encoding='latin-1')
    df3=pd.read_csv(data_path+"/TOTAL_NACIONAL_REG2.txt",sep="\t",encoding="latin-1")
    df4=pd.read_csv(data_path+"/destino_economico.csv",sep=";")
    return df,df2,df3,df4

