import PyPDF2
import os
import re


def sanitize(text):
    return text.strip(":").strip().replace("  ", " ")


def prettyprint(prefix, text):
    newtext = prefix + " " + sanitize(text)
    print(newtext, end="\n\n")
    return newtext


def extractSnippets(text, filename):
    try:
        summary = re.search(
            r"(?:summary[s]?[:]?[\s]?)(.*?)(?:objective|background|result|conclusion)", text, flags=re.IGNORECASE | re.MULTILINE)

        objective = re.search(r"(?:objective[s]?[:]?[\s]?)(.*?)(?:background|method|result|conclusion)", text,
                              flags=re.IGNORECASE | re.MULTILINE)

        background = re.search(r"(?:background[s]?[:]?[\s]?)(.*?)(?:method|result|conclusion)", text,
                               flags=re.IGNORECASE | re.MULTILINE)

        methods = re.search(
            r"(?:method[s]?[:]?[\s]?)(.*?)(?:result|conclusion)", text, flags=re.IGNORECASE | re.MULTILINE)

        results = re.search(
            r"(?:result[s]?[:]?[\s]?)(.*?)(?:conclusion)", text, flags=re.IGNORECASE | re.MULTILINE)

        conclusion = re.search(
            r"(?:conclusion[s]?[:]?[\s]?)(.*)", text, flags=re.IGNORECASE | re.MULTILINE)

        if summary:
            nt = prettyprint(prefix="SUMMARY\n", text=summary.group(1))
            open('abstract/' + filename.replace("pdf", "txt"),
                 'a').write(nt + "\n")
        if objective:
            nt = prettyprint(prefix="OBJECTIVE\n", text=objective.group(1))
            open('abstract/' + filename.replace("pdf", "txt"),
                 'a').write(nt + "\n")
        if background:
            nt = prettyprint(prefix="BACKGROUND\n", text=background.group(1))
            open('abstract/' + filename.replace("pdf", "txt"),
                 'a').write(nt + "\n")
        if methods:
            nt = prettyprint(prefix="METHODS\n", text=methods.group(1))
            open('abstract/' + filename.replace("pdf", "txt"),
                 'a').write(nt + "\n")
        if results:
            nt = prettyprint(prefix="RESULTS\n", text=results.group(1))
            open('abstract/' + filename.replace("pdf", "txt"),
                 'a').write(nt + "\n")
        if conclusion:
            nt = prettyprint(prefix="CONCLUSION\n", text=conclusion.group(1))
            open('abstract/' + filename.replace("pdf", "txt"),
                 'a').write(nt + "\n")
    finally:
        pass


directory = os.path.dirname(os.path.realpath(__file__)) + "/pdfs"
for filename in os.listdir(directory):
    if filename.endswith(".pdf"):
        fullFileName = os.path.join(directory, filename)
        pdfFileObj = open(fullFileName, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict=False)
        print(filename, end='\n\n')
        pageObj = pdfReader.getPage(0)
        text = pageObj.extractText()
        extractSnippets(text, filename)
        pdfFileObj.close()
    else:
        continue
