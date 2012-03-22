#!/usr/bin/env python
# coding: utf-8

import sqlite3
import os
import urllib
import shutil

MENDELEY_USER = "raphael.wimmer@ifi.lmu.de"
SYNC_TAGS = ["_read"]
BOOX_DIR = "/media/boox/mendeley/"

DB_PATH = os.path.expanduser("~/.local/share/data/Mendeley Ltd./Mendeley Desktop/" + MENDELEY_USER +  "@www.mendeley.com.sqlite")

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

documents_to_sync = set([])
for tag in SYNC_TAGS:
    sql_document_ids = cursor.execute("select documentId from DocumentTags where tag = '" + tag + "'")
    for docid in sql_document_ids:
        documents_to_sync.add(docid[0])

print documents_to_sync

hashes_to_sync = []
for docid in documents_to_sync:
    sql_file_hashes = cursor.execute("select hash from DocumentFiles where documentId = '%d'" % docid)
    for file_hash in sql_file_hashes:
        hashes_to_sync.append(file_hash[0])

print hashes_to_sync

files_to_sync = []
for file_hash in hashes_to_sync:
    sql_files = cursor.execute("select localUrl from Files where hash = '" + file_hash + "'")
    for file_name in sql_files:
        files_to_sync.append(file_name[0])

print files_to_sync

for file_url in files_to_sync:
    filename = urllib.url2pathname(file_url)
    print "Copying " + filename + " to " + BOOX_DIR
    shutil.copy(filename[7:], BOOX_DIR) # strip "file://"

print "done"


