import pandas as pd
import datetime
import numpy as np

#read csv and create dataframe
df = pd.read_csv('GoogleAPIMetadata.csv')
df.head()

df.columns
df.head()

#split data from shortcutDetails column and splits it by comma into two new columns
df[['targetID','targetType']] = df['shortcutDetails'].astype(str).str.split(', ', expand=True).reindex([0, 1], axis=1)
df.drop(['shortcutDetails'], axis=1, inplace=True)

#replace the google ID and mimeType with the data from the shortcutDetails column
df.google_id = np.where(df.targetID=='nan', df.google_id, df.targetID)
df.mimeType = np.where(df.targetType.isna(), df.mimeType, df.targetType)

#delete targetID and targetType columns
df = df.drop('targetID', axis=1)
df = df.drop('targetType', axis=1)

#write formatted to csv
df.to_csv("metadata_shortcuts.csv", index=False)
