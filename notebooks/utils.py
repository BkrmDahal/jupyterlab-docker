import re
import os

import shutil
import yaml
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import download
from nltk.tokenize import word_tokenize

##downoad packages
download('stopwords')
download('punkt')
download('wordnet')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

lemmatizer = WordNetLemmatizer()
strip_special_chars = re.compile("[^A-Za-z0-9 ]+")
stop_words = set(stopwords.words("english"))

#added the pdf mining
def allowed_file_invoice(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['pdf', 'jpg', 'jpeg', 'png', 'tif']

def clean_up_sentence(word):
    """clean any unwanted words and get root words"""
    return _lemmatiz_clean(_clean_str(word))

def _lemmatiz_clean(r, stop_words = stop_words):
    """remove stop words and let root word"""
    r = r.lower().replace("<br />", " ")
    r = re.sub(strip_special_chars, "", r.lower())
    if stop_words is not None:
        words = word_tokenize(r)
        filtered_sentence = []
        for w in words:
            w = lemmatizer.lemmatize(w)
            if w not in stop_words:
                filtered_sentence.append(w)
        return " ".join(filtered_sentence)
    else:
        return r
    
def _clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()

def read_config(file_name):
    """Read config file"""
    with open(file_name, 'r') as stream:
        try:
            configs=yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return configs

def top_n(x, n):
    """Get index of top n item from list"""
    top = sorted(range(len(x)), key=lambda i: x[i], reverse=True)[:n]
    prob = [x[i] for i in top]
    return top, prob

def delete_dirs(folder_name):
    """delete all the content of folder"""
    
    if isinstance(folder, str):
        shutil.rmtree(folder_name)
        os.makedirs(folder)
    elif isinstance(folder, list):
        for f in folder:
            shutil.rmtree(folder_name)
            os.makedirs(folder)
    else:
        raise TypeError("Input should be str or list ")
        
def make_dirs(folder):
    """make folder if it doesnot exist"""
    if isinstance(folder, str):
        if not os.path.exists(folder):
            os.makedirs(folder)
    elif isinstance(folder, list):
        _ = [ os.makedirs(i) for i in folder if not os.path.exists(i) ]
    else:
        raise TypeError("Input should be str or list ")
        
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ['pdf']

    
def clean_str(string):
    """
    Tokenization/string cleaning for all datasets'
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()
    
needed_values = ['gstin', 'total', 'description', 'rate', 'amount', 'name', 'date', 'invoice']