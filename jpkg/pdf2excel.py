#from PyPDF2 import PdfReader

#data   = []
#reader = PdfReader('DuP Tax 2012440.pdf')
#page   = reader.pages[0]
#text   = page.extract_text().split('\n')
#print(text)
#index  = [ i+1 for i, x in enumerate(text) if x == 'PERM PARC NO   ASSESSEES NAME TOT AMT DUE' ]
#print(index)
#for i in range(len(index)):
#    data.append(text[index[i]])
#print(data)

#import re
from PyPDF2 import PdfReader

class RecordDat:
    def __init__(self):
        self.township = None
        self.section = None
        self.records = []

def print_file(recordArray):
    for i in range(len(recordArray)):
        print(recordArray[i].township)
        for x in range(len(recordArray[i].records)):
            lineText = recordArray[i].township
            # print(lineText)
            if lineText:
                lineText.append(';')
                lineText.append(recordArray[i].section)
                lineText.append(';')
                lineText.append(recordArray[i].records[x])
                # print(lineText)

def parse_file(filename):
    data, recordArray = [], None
    reader = PdfReader(filename)
    for t in range(len(reader.pages)):
        page = reader.pages[t]
        text = page.extract_text().split('\n')
        # print(text)

        recordArray = []
        recordDat = RecordDat()
        for i, x in enumerate(text):
            townshipIndex = x.find("TOWNSHIP")
            sectionIndex = x.find("SECTION")
            parcelDelimiterCount = x.count("-")
            if townshipIndex != -1:
                recordDat.township = text[i].split(' ')[1]
#                print('*=================')
#                print(recordDat.township)
            elif sectionIndex != -1:
                 recordDat.section = text[i].split('  ')[1]
#                 print(recordDat.section)
                 i = i + 2
            elif parcelDelimiterCount == 3:
#                 print(x)
                 result = split_letter_and_number(x)
                 if result:
                     recordDat.records.append(';'.join(map(str,result)))
                     # print(recordDat.records)
                     # print("nn")
                 # recordDat.records.append(delimiter.join(x.split()))
                 # print (recordDat.records)
                 if recordDat.records:    recordArray.append(recordDat)
#            recordDat = RecordDat()
    print("final size:")
    print(len(recordArray))
    for i in range(len(recordArray)):
        print(recordArray[i].township)
    print_file(recordArray)

def split_letter_and_number(input_string):
    parts = input_string.split()
    name = parts[1:-1]
    my_list = [parts[0], name, parts[-1]]
    print(my_list)
    return my_list

    # index = [i + 1 for i, x in enumerate(text) if x == 'DELINQUENT TAX LIST OF GENERAL TAXES']
    # print("nn")
    # print(index, x)

    # index = [i + 1 for i, x in enumerate(text) if x == 'DELINQUENT TAX LIST OF GENERAL TAXES']
    # print("nn")
    # print(index)
    #
    #
    # index = [ i+1 for i, x in enumerate(text) if x == 'PERM PARC NO ASSESSEES NAME TOT AMT DUE']
    # print("nn")
    # print(index)

    # for i in range(len(index)):
    #     data.append(text[index[i]])
    #     print(data)


if __name__ == '__main__':
    parse_file('DuP Tax 2012440.pdf')
