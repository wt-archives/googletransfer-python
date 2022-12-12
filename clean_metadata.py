import pandas as pd
import datetime
import numpy as np

#read csv and create dataframe
df = pd.read_csv('GoogleTestMetadata.csv')
df.head()

#rename columns and create new dataframe
df.columns
df.head()

df2 = df.rename(columns = {'identifier' :'Subject', 'file_name' :'filename', 'original_file_name' :'Title', 'date_created':'CreateDate',  'google_id' :'Source', 'google_parent_id' :'Relation', 'mimeType' :'Type', 'size' :'Coverage', 'owners' :'Creator', 'lastModifyingUser' :'Contributor'}, inplace = False)
df2.head()

#list columns
df2.columns = ['Subject', 'filename', 'description', 'Title', 'folder',	'CreateDate', 'date_last_modified', 'checksum_md5', 'closure_type', 'closure_period', 'closure_start_date', 'foi_exemption_code', 'foi_exemption_asserted', 'title_public', 'title_alternate', 'description_public', 'description_alternate', 'Source', 'Relation', 'Rights', 'Publisher', 'Type', 'Coverage', 'archivist_note', 'file_name_note', 'original_identifier', 'Language', 'sharingUser', 'Creator', 'Contributor']

#clean metadata
df2['Coverage'] = df2['Coverage'].str.replace("-","", regex=True)
df2['Subject'] = df2['Subject'].str.replace("/","; ", regex=True)
df2['Subject'] = df2['Subject'].str.replace("content; ","", regex=True)
df2['Subject'] = df2['Subject'].str.replace(r'\s\S*\.\S*', '', regex=True)
df2['Subject'] = df2['Subject'].str.rstrip(' ')
df2['Subject'] = df2['Subject'].str.rstrip(';')
df2['Subject'] = df2['Subject'].str.replace("_"," ", regex=True)
df2['Description'] = df2['description'].apply(str) + ' ' + df2['archivist_note'].apply(str) + ' ' + df2['original_identifier'].apply(str)+ ' ' + df2['file_name_note'].apply(str)
df2['Description'] = df2['Description'].replace(np.NaN, '', regex=True, inplace = True)
#df2['Description'] = df2['Description'].str.replace("nan ","", regex=True).str.replace("nan","", regex=True)
df2['CreateDate'] = df2['CreateDate'].apply(str) + '; modified ' + df2['date_last_modified'].apply(str)
df2['Contributor'] = df2['Contributor'].apply(str) + '; ' + df2['sharingUser'].apply(str)
df2['Source'] = "google id: " + df2['Source'].astype(str)
df2['Contributor']= "last modified by: " + df2['Contributor'].astype(str)
df2['Relation'] = "google parent folder id: " + df2['Relation'].astype(str)
df2['Contributor'] = df2['Contributor'].str.replace("{::, ","", regex=True).str.replace(" }","", regex=True)

#duplicates filename column and strips all but file extension into 'format' column
df2['Format'] = df2.loc[:, 'filename']
df2['Format'] = df2['Format'].str.split('\.').str[-1].str.strip()


#drops rows which are folder-level entries
df2 = df2[df2.folder != 'folder']

#drops columns which have been joined into others and unused columns
df2 = df2.drop(['description', 'folder', 'date_last_modified', 'checksum_md5', 'archivist_note', 'original_identifier', 'file_name_note', 'sharingUser', 'closure_type', 'closure_period', 'closure_start_date', 'foi_exemption_code', 'foi_exemption_asserted', 'title_public', 'title_alternate', 'description_public', 'description_alternate'], axis = 1, inplace = False)

#write formatted to csv
df2.to_csv("metadata_cleaned.csv", index=False)
