import pandas as pd
import datetime
import numpy as np

#read csv and create dataframe
df = pd.read_csv('metadata_cleaned.csv')
df.head()

#rename columns and create new dataframe
df.columns
df.head()

#list columns
df.columns = ['Subject', 'filename', 'Title', 'CreateDate', 'Source', 'Relation', 'Rights', 'Publisher', 'Type', 'Coverage', 'Language', 'Creator', 'Contributor', 'Description', 'Format']

#name top-level parent folder
df['Subject'] = df['Subject'].str.replace("ParentFolderName","hello", regex=True)

#write formatted to csv
df.to_csv("metadata_FINAL.csv", index=False)
