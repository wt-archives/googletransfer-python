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
df.columns = ['Subject', 'filename', 'Title', 'Date', 'Source', 'Relation', 'Rights', 'Publisher', 'Type', 'Coverage', 'Language', 'Creator', 'Contributor', 'Identifier', 'Description', 'Format']

#name top-level parent folder
df['Subject'] = df['Subject'].str.replace("ParentFolderName","2020-2021", regex=True)

#reorder columns alphabetically
df = df.reindex(sorted(df.columns), axis=1)
df = df[ ['filename'] + [ col for col in df.columns if col != 'filename' ] ]

#write formatted to csv
df.to_csv("metadata_FINAL.csv", index=False)
