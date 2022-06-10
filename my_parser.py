import email
import os
import glob
import pandas
from email.parser import BytesParser
from email.parser import Parser
from email import policy
import codecs
import mailparser
import chardet
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string


# Функция которая принимает путь к папке с письмами и записывает их содержимое
def parse(path, type):
    text = ''
    line = []
    data = []
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')  # Убираем HTML
    eml_files = glob.glob(path + '/*.eml')  # get all .eml files in a list
    for eml_file in eml_files:
        with codecs.open(eml_file, 'r', encoding="ISO-8859-1") as stream:
            parser = Parser()
            message = parser.parse(stream)

        for part in message.walk():
            if part.get_content_type().startswith('text/plain'):
                enc = (chardet.detect(part.get_payload(decode=True)))
                if enc['encoding'] is not None:
                    text = (part.get_payload(decode=True).decode(enc['encoding']))
                    text = re.sub(CLEANR, ' ', text)
                    text = re.sub(r'http\S+', '', text)
                    text = text.replace('\n', ' ').replace('\r', ' ')
                    line = [type, text]
                    data.append(line)
                else:

                    print (eml_file)
    return data
