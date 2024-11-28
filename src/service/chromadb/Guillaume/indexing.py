import os
from importlib.metadata import files

import pypdf as pdfr
import csv

def indexing_file(dir_to_search):
    list_of_all_file = dict()
    files_directory = os.listdir(dir_to_search)
    temp_name_file = ""
    files =[]
    directories = []

    #indexing files and directory
    for i in files_directory:
        if os.path.isdir(i):
            #if it's a directory it's added to directories
            directories.append(i)
        else:
            #if it's a file it's append here
            files.append(i)

    #
    for i in files:
        for j in i:
            if j != '.':
                temp_name_file += j
            else:
                list_of_all_file[temp_name_file] = i
                temp_name_file = ""
        temp_name_file = ""

    return list_of_all_file , directories


def indexing_csv_files(all_files):
    files = all_files
    csv_files = []
    csv_dictionnary = dict()
    temp_name_file = ""
    for i in files:

        if i.find('.csv') != -1:
            csv_files.append(i)

    for i in csv_files:
        for j in i:
            if j != '.':
                temp_name_file += j
            else:
                csv_dictionnary[temp_name_file] = i
                temp_name_file = ""
        temp_name_file = ""
    return csv_dictionnary




def indexing_pdf_files(dir_to_search):
    files = os.listdir(dir_to_search)
    pdf_dictionnary = dict()
    temp_name_file = ""
    pdf_files = []
    for i in files:
        if i.find(".pdf") != -1:
            pdf_files.append(i)

    for i in pdf_files:
        for j in i:
            if j != '.':
                temp_name_file += j
            else:
                pdf_dictionnary[temp_name_file] = i
                temp_name_file = ""
        temp_name_file = ""
    return  pdf_dictionnary

