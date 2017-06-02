import os

from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

from subprocess import call #decrypt pdf

def decrypt_pdf(input_path, output_path, file_name):
    input_file = input_path + file_name
    output_file = output_path + file_name
    call('qpdf --password=%s --decrypt %s %s' % ('', input_file, output_file), shell=True)

def parse_pdf(input_path, file_name):
    input_file = input_path + file_name
    fp = open(input_file, 'rb')

    parser = PDFParser(fp)
    doc = PDFDocument()

    parser.set_document(doc)
    doc.set_parser(parser)

    doc.initialize('')

    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        resource = PDFResourceManager()
        laparam = LAParams()
        device = PDFPageAggregator(resource, laparams=laparam)
        interpreter = PDFPageInterpreter(resource, device)

        for page in doc.get_pages():
            interpreter.process_page(page)
            layout = device.get_result()

            for line in layout:
                if (isinstance(line, LTTextBoxHorizontal)):
                    output_file = input_path + file_name[0:len(file_name) - 4] + '.txt'
                    with open(output_file, 'a') as file:
                        output = line.get_text().encode("utf8").decode("cp950", "ignore")
                        file.write(output + '\n')
                # if hasattr(out, 'get_text'):
                #     print(out.get_text())

def main():
    data_dir = '../Data/'
    output_dir = '../Data/HarryPotter/'

    #read all of file from folder
    file_data = []
    for file_name in os.listdir(data_dir):
        # print('loading: %s' % file_name)
        file_data.append(file_name)
    print('All of file:', file_data)

    #filter,  decrypt pdf and convert PDF to TEXT
    filter_list = filter(lambda x:x.endswith('.pdf'), file_data)
    print('Filter File')
    for file_name in filter_list:
        print('Decrypt File:', file_name)
        decrypt_pdf(data_dir, output_dir, file_name)
        print('---- convert PDF to TEXT -----')
        parse_pdf(output_dir, file_name)
        print('Finish:', file_name, '!!!')

if __name__ == '__main__':
    main()

# http://blog.csdn.net/PianoOrRock/article/details/70666286
# http://benlog.logdown.com/posts/308361-read-all-files-in-a-folder-using-python
# http://lionrex.pixnet.net/blog/post/117196706-%5Bpython%5D-%27cp950%27-%2C-illegal-%2C-unicodeencodeerror