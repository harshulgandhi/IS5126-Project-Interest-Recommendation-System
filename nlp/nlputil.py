'''
Created on May 10, 2014

@author: vdw
'''
#import guess_language
from nltk.corpus import stopwords
import re
from nltk.tokenize import word_tokenize
import time
import unicodedata
import datetime as dt
import HTMLParser
from tokenizer import Tokenizer, TOKEN_CLASS_URL, TOKEN_CLASS_NUMBER,\
    TOKEN_CLASS_SPECIAL_TERM_USER, TOKEN_CLASS_SPECIAL_TERM_TOPIC,\
    TOKEN_CLASS_ALPHANUM

STOPWORDS_ENGLISH = set(stopwords.words("english"))

class NlpUtilities: 
    
    def __init__(self):
        self.alphanum_pattern = re.compile('[\s\W_]+', re.UNICODE)
        self.html_parser = HTMLParser.HTMLParser()
    
    def remove_stopwords(self, word_list):
        #return [w for w in word_list if w.isupper() or not w.lower() in STOPWORDS_ENGLISH]
        return [w for w in word_list if w.lower() not in STOPWORDS_ENGLISH]
    
    def is_stop_word(self, word):
        if word in STOPWORDS_ENGLISH:
            return True
        return False
    
    def asciify_word(self, word):
        return ''.join([char if ord(char) < 128 else ' ' for char in word])
            
    def asciify_word_list(self, word_list):
        return [ ''.join([char if ord(char) < 128 else ' ' for char in w]) for w in word_list  ]
    
    def remove_duplicates(self, s, character_list):
        for c1 in character_list:
            c1 = re.escape(c1)
            s = re.sub('[\b'+c1+'\b]{3}', ' ', s)
            print s.decode("string-escape")
        return s
    
    def remove_html_tags(self, s):
        s = re.sub('<[^>]*>', '', s)
        return s
    
    def remove_all_duplicates(self, s):
        s = re.sub(r'(.)\1+', r'\1\1', s)
        return s
        
    def ascii_simplify(self, s):
        return unicodedata.normalize('NFD', s).encode('ascii', 'ignore')
        
    def replace_repeated_letters(self, s, min_repeated_count, replace_count):
        replace_string = r''
        for i in range(0, replace_count):
            replace_string += r'\1'
        s = re.sub(r'(.)\1{'+str(min_repeated_count)+',}', replace_string, s)
        return s
        
    def replace_word(self, s, search, replacement):
        return re.sub(r'\b' + search + r'\b', replacement, s)
        
    def alphanumify(self, s):
        return self.alphanum_pattern.sub('', s) 
        
    def trim_all(self, s):
        return re.sub(' +',' ', s)
    
    def is_ascii(self, s):
        try:
            s.decode('ascii')
        except:
            return False
        else:
            return True
        
    def convert_camelcase(self, s):
        tmp = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', s)
        return re.sub('([a-z0-9])([A-Z])', r'\1 \2', tmp)
        
    def simplify_phrase(self, phrase, do_remove_stopwords):
        if do_remove_stopwords == True:
            phrase = ' '.join(self.remove_stopwords(phrase.split()))
            
        tokenizer = Tokenizer(phrase)
        tokenizer.tokenize_as_tweet()
        phrase = tokenizer.generate_minimized_document(token_list=None, valid_token_list=[TOKEN_CLASS_ALPHANUM, TOKEN_CLASS_SPECIAL_TERM_TOPIC, TOKEN_CLASS_SPECIAL_TERM_USER, TOKEN_CLASS_NUMBER, TOKEN_CLASS_URL])
            
        mapping = {}
        phrase_mod = []
        for word in phrase.split():
            word_mod = word 
            #word_mod = re.sub('[\']', '', word_mod)
            word_mod = re.sub('(\'s)', 's', word_mod)
            word_mod = re.sub('[-,&._]', '', word_mod)
            word_mod = re.sub('[()\[\]]', '', word_mod)
            word_mod = re.sub(r'\([^)]*\)', '', word_mod)
            word_mod = re.sub(' +',' ', word_mod)
            word_mod = word_mod.strip()
            phrase_mod.append(word_mod)
            #mapping[word_mod] = word
        phrase_simplified = ' '.join(phrase_mod)
        phrase_simplified = re.sub(' +',' ', phrase_simplified)
        mapping[phrase_simplified] = phrase 
        return phrase_simplified, phrase, mapping

    def is_alphanum(self, s):
        return re.match('^[\w]+$', s) is not None
    
#     def is_valid_tweet(self, tweet_json, check_if_ascii=True, remove_link_tweets=False, lang=['en'], min_length=0):    
#         if tweet_json.get('retweeted_status') is not None:
#             return False
#         text = tweet_json['text']
#         if remove_link_tweets == True:
#             if 'http' in text:
#                 return False
#         if len(text) < min_length:
#             return False
#         if check_if_ascii == True:
#             if not self.is_ascii(text):
#                 return False
#         result = guess_language.guessLanguage(text)
#         if result not in lang:
#             return False
#         return True
#     
    def unescape_html(self, text):
        return self.html_parser.unescape(text)

    #this will be called before remove stop words and replace repeated letters
    def clean_tweet(self, text):
        text = text.replace('\r\n', ' ')
        text = text.replace('\n', ' ')
        text = re.sub( '\s+', ' ', text).strip()
        return text
#print remove_extra_spaces('asd     asd  ')
#print alphanumify(' asd as; asd as (sddsd) -as ')
#s = ' I don\'t know your implementation of the algorithm, but I would find it the most sensible implementation. Using that, you can expand it to fit your needs. If this is what was your issue, I see Samuele has already expanded my comment into an answer: I\'d accept it, and build on that.'
#print s
#s = remove_stopwords(s)
#print s

#print calculate_tf_vector(s)

#print remove_all_duplicates('I\'m sooooo pissssssssssed!!!!!')
#print replace_repeated_letters('looool', 3, 1)


if __name__ == "__main__":
    #print STOPWORDS_ENGLISH
    nlp = NlpUtilities()
    #s = 'Sweethearts 23 get MH347-3 along well with my sibling ..________ (with @NindySelvo at My Crib @ LaCasa) [pic] _ https://t.co/L7Wi3OW5lT'
    #simplified_name, old, mapping = nlp.simplify_phrase(s, do_remove_stopwords=False)
    #print s
    #print simplified_name
    print nlp.replace_repeated_letters('Hiii whats uppp tomorrrrow', 2, 1)
    #print nlp.simplify_phrase(s, do_remove_stopwords=True)
    #print nlp.simplify_phrase(s, do_remove_stopwords=False)
    #print nlp.is_alphanum('d')
