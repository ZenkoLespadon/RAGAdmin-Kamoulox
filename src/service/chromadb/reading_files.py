import os.path

import pypdf


def reading_files(dir_to_search, files, list_files):
    pdf = []
    for i in list_files:
        path = os.path.join(dir_to_search, list_files[i])
        if i == files:
            pdf.append(pypdf.PdfReader(path))
    return pdf