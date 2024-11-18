import os
import pypdf as pdfr

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


def indexing_pdf_files(all_files):
    files = all_files
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

