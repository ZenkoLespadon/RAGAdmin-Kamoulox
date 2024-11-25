import pypdf

def pdf_to_text(pdf):
    final_doc = []
    for i in range(len(pdf.pages)):
        final_doc.append(pdf.pages[i].extract_text())
    return final_doc