import pandas as pd
import numpy as np
import os
import ast
import datetime


filelist = pd.read_csv('GoogleAPIMetadata.csv', converters={'google_parent_id': ast.literal_eval})
filelist = filelist.explode('google_parent_id')
filelist = filelist.drop_duplicates()
filelist = filelist.reset_index()
filelist['folder'] = ''
filelist['original_file_name'] = filelist['file_name']
filelist['file_name_note'] = ''
filelist['archivist_note'] = ''
filelist[''] = ''
filelist['sharingUser'] = filelist['sharingUser']
filelist['owner'] = filelist['owners']
filelist['lastModifyingUser'] = filelist['lastModifyingUser']
content = {'identifier': ['content/'], 'file_name': ['content'], 'date_created': [datetime.datetime.now().isoformat()], 'date_last_modified': [datetime.datetime.now().isoformat()], 'folder':['folder'], 'sharingUser': ['sharingUser'], 'owners': ['owners'], 'lastModifyingUser': ['lastModifyingUser']} #adding content folder in as this is the folder which it has been run from because it does not get picked up by API
content = pd.DataFrame(content, columns = ['identifier','filename','date_created','date_last_modified','folder','sharingUser','owners','lastModifyingUser'])

def get_parents(): #dictionary which takes list of google ID and parent ID, checks if parent ID is in list, adds to a parents list if so, then creates the identifier row with list of all parent IDs related to google ID
    parentslist = []
    filelist_dict = dict(zip(filelist.google_id, filelist.google_parent_id))
    for parent in filelist['google_parent_id']:
        T1 = ()
        while parent in filelist_dict.keys():
            for k, v in filelist_dict.items():
                if parent == k:
                        T1 = (k,) + T1
                        parent = v
        parentslist.append(T1)
    filelist['identifier'] = parentslist

get_parents()

def rename_googledocs(): #renames google docs with appropriate new filename for download, always leaves a note to state which format it is converting it to.
    filelist['file_name'] = np.where(filelist.mimeType == 'application/vnd.google-apps.document', filelist['file_name'] + '.docx', filelist['file_name'])
    filelist['archivist_note'] = np.where(filelist.mimeType == 'application/vnd.google-apps.document', 'This file was originally a Google Doc format and has been converted to an Microsoft Office Word file. ', filelist['archivist_note'])
    filelist['file_name'] = np.where(filelist.mimeType == 'application/vnd.google-apps.spreadsheet', filelist['file_name'] + '.xlsx', filelist['file_name'])
    filelist['archivist_note'] = np.where(filelist.mimeType == 'application/vnd.google-apps.spreadsheet', 'This file was originally a Google Sheets format and has been converted to an Microsoft Excel file. ', filelist['archivist_note'])
    filelist['file_name'] = np.where(filelist.mimeType == 'application/vnd.google-apps.presentation', filelist['file_name'] + '.pptx', filelist['file_name'])
    filelist['archivist_note'] = np.where(filelist.mimeType == 'application/vnd.google-apps.presentation', 'This file was originally a Google Slides format and has been converted to an Microsoft Powerpoint file. ', filelist['archivist_note'])
    filelist['file_name'] = np.where(filelist.mimeType == 'application/vnd.google-apps.drawing', filelist['file_name'] + '.png', filelist['file_name'])
    filelist['archivist_note'] = np.where(filelist.mimeType == 'application/vnd.google-apps.drawing', 'This file was originally a Google Draw file and has been converted to a PNG file. ', filelist['archivist_note'])
    filelist['file_name'] = np.where(filelist.mimeType == 'application/vnd.google-apps.jam', filelist['file_name'] + '.pdf', filelist['file_name'])
    filelist['archivist_note'] = np.where(filelist.mimeType == 'application/vnd.google-apps.jam', 'This file was originally a Google Jamboard format and has been converted to a PDF file. ', filelist['archivist_note'])
rename_googledocs()


def rename_problem_files(): #renames characters not allowed in file systems with, always leaves a note to say when filename has changed.
    filelist['file_name'] = filelist['file_name'].str.replace("/","_", regex=True)
    filelist['file_name'] = filelist['file_name'].str.replace("\\", "_", regex=True)
    filelist['file_name'] = filelist['file_name'].str.replace(":", "-", regex=True)
    filelist['file_name'] = filelist['file_name'].str.replace("*", "", regex=True)
    filelist['file_name'] = filelist['file_name'].str.replace("?", "", regex=True)
    filelist['file_name'] = filelist['file_name'].str.replace('"', '', regex=True)
    filelist['file_name'] = filelist['file_name'].str.replace(">", "_", regex=True)
    filelist['file_name'] = filelist['file_name'].str.replace("<", "_", regex=True)
    filelist['file_name'] = filelist['file_name'].str.replace("|", "_", regex=True)
    filelist['file_name'] = filelist['file_name'].str.replace(" ", "_", regex=True)
    filelist['file_name'] = filelist['file_name'].str.replace("&", "_", regex=True)
    filelist['file_name'] = filelist['file_name'].str.replace("(", "", regex=True)
    filelist['file_name'] = filelist['file_name'].str.replace(")", "", regex=True)
    filelist['file_name'] = filelist['file_name'].str.replace(",", "", regex=True)
    filelist['file_name'] = filelist['file_name'].str.replace("'", "", regex=True)
    filelist['file_name'] = filelist['file_name'].str.replace(".", "-", regex=True)
    filelist['file_name'] = filelist['file_name'].str.replace("_-_", "_", regex=True)
    filelist['file_name'] = filelist['file_name'].str.replace("-_", "_", regex=True)
    filelist['file_name'] = filelist['file_name'].str.replace("__", "_", regex=True)
    filelist['file_name'] = filelist['file_name'].str.replace("___", "_", regex=True)
    filelist['file_name'] = filelist['file_name'].str.replace("--", "-", regex=True)
    filelist['file_name'] = filelist['file_name'].str.replace("-docx", ".docx", regex=True)
    filelist['file_name'] = filelist['file_name'].str.replace("-pdf", ".pdf", regex=True)
    filelist['file_name'] = filelist['file_name'].str.replace("-doc", ".doc", regex=True)
rename_problem_files()


def rename_duplicates(): #renames duplicate files with numerical number
    filelist['file_name'] = filelist['file_name'].astype(str)
    filesplit = pd.DataFrame([os.path.splitext(f) for f in filelist.file_name], columns=['Name', 'Ext'])
    c = filelist.groupby(["file_name", 'google_parent_id']).cumcount()
    c = c.astype(str)
    filelist['file_name'] = filesplit['Name'] + '(' + c + ')' + filesplit['Ext']
    filelist['file_name'] = filelist['file_name'].str.replace("\(0\)", "",regex = True)
rename_duplicates()

def rename_folders(): #takes the identifier converts google id to file or folder name, then adds slashes, removes speech marks, creates folder column with folder or file entries depending on mime type.

    filelist['identifier'] = filelist['identifier'].astype(str)
    mime = filelist.groupby('mimeType')
    foldernumbers = filelist['mimeType'].str.contains('application/vnd.google-apps.folder').sum()
    if foldernumbers>0:
        folders = mime.get_group('application/vnd.google-apps.folder')
        folder_dict =  dict(zip(folders.google_id, folders.file_name))

        for k, v in folder_dict.items():
            filelist['identifier'] = filelist['identifier'].str.replace(k,v)

    filelist['identifier'] = filelist['identifier'].str.lstrip("('").str.replace("'\)", '/', regex=True).str.replace("', '", "/", regex=True).str.replace("',\)", '/', regex=True).str.lstrip(')')
    filelist['identifier'] = filelist['identifier'] + filelist['file_name']
    filelist['identifier'] = np.where(filelist.mimeType == 'application/vnd.google-apps.folder', filelist['identifier'] + '/', filelist['identifier'])
    filelist['identifier'] = 'ParentFolderName/' + filelist['identifier']
    filelist['folder'] = np.where(filelist.mimeType == 'application/vnd.google-apps.folder', 'folder', filelist['folder'])
    filelist['folder'] = np.where(filelist.mimeType != 'application/vnd.google-apps.folder', 'file', filelist['folder'])

rename_folders()

def strip_user(): #strips unneccessary data from the lastModifyingUser field, including kind, photoLink, me, and permissionId. Leaves displayName and emailAddress separated by comma
    filelist['lastModifyingUser'] = filelist['lastModifyingUser'].str.replace("{'kind': 'drive#user', 'displayName': '","", regex=True)
    filelist['lastModifyingUser'] = filelist['lastModifyingUser'].str.replace("', 'photoLink':", "", regex=True)
    filelist['lastModifyingUser'] = filelist['lastModifyingUser'].str.replace("'me': True, 'permissionId': ", "", regex=True)
    filelist['lastModifyingUser'] = filelist['lastModifyingUser'].str.replace("'me': False, 'permissionId': ", "", regex=True)
    filelist['lastModifyingUser'] = filelist['lastModifyingUser'].str.replace(", 'emailAddress': '", ", ", regex=True)
    filelist['lastModifyingUser'] = filelist['lastModifyingUser'].str.replace("'[^']+'", "" , regex=True)
    filelist['lastModifyingUser'] = filelist['lastModifyingUser'].str.replace(" , ", "" , regex=True)
    filelist['lastModifyingUser'] = filelist['lastModifyingUser'].str.replace("'}", "" , regex=True)

strip_user()

content = pd.concat([content, filelist], sort=True)

def convert_to_tna(): #adds in some standard metadata fields, converts date to xdatetime
    del content['index']
    content['closure_type'] = ''
    content['closure_period'] = ''
    content['closure_start_date'] = ''
    content['foi_exemption_code'] = ''
    content['foi_exemption_asserted'] = ''
    content['title_public'] = ''
    content['title_alternate'] = ''
    content['description_public'] = ''
    content['description_alternate'] = ''
    content['description'] = ''
    content['Language'] = 'English'
    content['Rights'] = ''
    content['legal_status'] = 'Public Record(s)'
    content['Publisher'] = 'Esther Duke Archives at Westtown School'
    content['date_last_modified'] = pd.to_datetime(content["date_last_modified"])
    content['date_last_modified'] = content.date_last_modified.map(lambda x: datetime.datetime.strftime(x, '%Y-%m-%dT%H:%M:%SZ'))
    content['date_created'] = pd.to_datetime(content["date_created"])
    content['date_created'] = content.date_created.map(lambda x: datetime.datetime.strftime(x, '%Y-%m-%dT%H:%M:%SZ'))
    content['original_identifier'] = ''
    content['ID'] = ''

convert_to_tna()

content = content.sort_values('identifier') #sorted by identifer (as DROID would do)
content = content[
        ['identifier', 'file_name','description','original_file_name', 'folder', 'date_created', 'date_last_modified','checksum_md5', 'closure_type',
         'closure_period', 'closure_start_date', 'foi_exemption_code', 'foi_exemption_asserted', 'title_public',
         'title_alternate','description_public','description_alternate',  
         'google_id', 'google_parent_id', 'Rights', 'Publisher', 'mimeType','size', 'archivist_note','file_name_note','original_identifier', 'Language', 'sharingUser', 'owners', 'lastModifyingUser', 'ID']]
content.to_csv('GoogleTestMetadata.csv', index=False)