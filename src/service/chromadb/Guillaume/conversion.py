import pypdf

def pdf_to_text(pdf):
    docs = []
    for files  in pdf:
        final_doc = []
        for i in range(len(files.pages)):
            final_doc.append(files.pages[i].extract_text())
        docs.append(final_doc)
    return docs