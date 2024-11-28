import os.path

import pypdf
from pypdf import PdfReader


def reading_files_pdf(dir_to_search, files, list_files):
    pdf = []
    for i in list_files:
        path = os.path.join(dir_to_search, list_files[i])
        if i == files:
            pdf.append(pypdf.PdfReader(path))
    return pdf

def getting_data_from_pdf(dir_to_search, list_files):
    pdf = []

    for key, value in list_files.items():
        path = dir_to_search+"/"+value
        if os.path.exists(path) and  os.path.getsize(path) > 0:
            pdf.append(PdfReader(path))

    return pdf