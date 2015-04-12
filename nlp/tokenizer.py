'''
Created on Jun 3, 2014

@author: christian
'''
import re
import string
from operator import pos

PUNCTUATION_MARKS__TERMINAL_POINTS = '.!?'
PUNCTUATION_MARKS__PAUSING_POINTS = ',:;'

EMOTICONS_FIXED_PATTERNS = ':-) :) :o) :] :3 :c1) :> =] 8) =) :} :^) :D 8-D 8D x-D xD X-D XD =-D =D =-3 =3 B^D ^^'.split()
EMOTICONS_GENERIC_PATTERN_EYES = ':;8BX='
EMOTICONS_GENERIC_PATTERN_NOSES = '-~\'^'
EMOTICONS_GENERIC_PATTERN_MOUTHS = ')(/\|DP'



TOKEN_CLASS_UNKNOWN = 0
TOKEN_CLASS_WHITESPACE = 1
TOKEN_CLASS_ALPHANUM = 10
TOKEN_CLASS_PUNCTUATION_TERMINAL_POINTS = 20
TOKEN_CLASS_PUNCTUATION_TERMINAL_POINTS_REPEATED = 21
TOKEN_CLASS_PUNCTUATION_PAUSING_POINTS = 30
TOKEN_CLASS_PUNCTUATION_PAUSING_POINTS_REPEATED = 31
TOKEN_CLASS_USER_NAME = 40
TOKEN_CLASS_TOPIC = 50
TOKEN_CLASS_URL = 60
TOKEN_CLASS_EMAIL = 65
TOKEN_CLASS_SPECIAL_TERM_USER = 70
TOKEN_CLASS_SPECIAL_TERM_TOPIC = 71
TOKEN_CLASS_NUMBER = 80
TOKEN_CLASS_EMOTICON = 90

TOKEN_CLASS_IN_VOCABULARY_WORD = 100
TOKEN_CLASS_SLANG = 110
TOKEN_CLASS_WAS_SLANG = 111
TOKEN_CLASS_IN_PLACE_VOCABULARY_WORD = 120
TOKEN_CLASS_NAMED_ENTITY_CANDIDATE = 130

TOKEN_CLASS_HTML_ENTITY = 150
TOKEN_CLASS_UNICODE = 160

TOKEN_CLASS_NON_ASCII = 200

class Tokenizer:
    
    def __init__(self, string):
        self.__raw_string = string
        self.__char_map = []
        self.__init_char_map()
        self.__token_list = []
    
    def __init_char_map(self):
        if self.__raw_string is not None:
            for c1 in self.__raw_string:
                self.__char_map.append(TOKEN_CLASS_UNKNOWN)
    
    def __set_token_class(self, start_pos, end_pos, token_class, overwrite=False):
        if not overwrite:
            if self.__is_partially_known(start_pos, end_pos):
                return
        for pos in range(start_pos, end_pos):
            self.__char_map[pos] = token_class
    
    def __is_partially_known(self, start_pos, end_pos):
        for pos in range(start_pos, end_pos):
            if self.__char_map[pos] != TOKEN_CLASS_UNKNOWN:
                return True
        return False
    

    
    def tokenize_as_tweet(self):
        if self.__raw_string is not None:
            self.__match_whitespaces(TOKEN_CLASS_WHITESPACE)
            self.__match_unicode_strings(TOKEN_CLASS_UNICODE)
            self.__match_urls(TOKEN_CLASS_URL)
            self.__match_emails(TOKEN_CLASS_EMAIL)
            self.__match_special_twitter_concepts('@', TOKEN_CLASS_SPECIAL_TERM_USER)
            self.__match_special_twitter_concepts('#', TOKEN_CLASS_SPECIAL_TERM_TOPIC)
            self.__match_html_entities(TOKEN_CLASS_HTML_ENTITY)
            self.__match_numbers(TOKEN_CLASS_NUMBER)
            self.__match_emoticons(TOKEN_CLASS_EMOTICON)
            self.__match_repeated_chars(PUNCTUATION_MARKS__TERMINAL_POINTS, TOKEN_CLASS_PUNCTUATION_TERMINAL_POINTS_REPEATED)
            self.__match_repeated_chars(PUNCTUATION_MARKS__PAUSING_POINTS, TOKEN_CLASS_PUNCTUATION_PAUSING_POINTS_REPEATED)
            self.__match_puncuation_marks(PUNCTUATION_MARKS__TERMINAL_POINTS, TOKEN_CLASS_PUNCTUATION_TERMINAL_POINTS)
            self.__match_puncuation_marks(PUNCTUATION_MARKS__PAUSING_POINTS, TOKEN_CLASS_PUNCTUATION_PAUSING_POINTS)
            self.__match_alphanumeric_words(TOKEN_CLASS_ALPHANUM)
            self.__match_selected_characters('&@*', TOKEN_CLASS_ALPHANUM)
            self.__match_nonascii_characters(TOKEN_CLASS_NON_ASCII)
            self.__generate_token_list()

    def tokenize(self):
        self.__match_whitespaces(TOKEN_CLASS_WHITESPACE)
        self.__match_urls(TOKEN_CLASS_URL)
        self.__match_emails(TOKEN_CLASS_EMAIL)
        self.__match_html_entities(TOKEN_CLASS_HTML_ENTITY)
        self.__match_numbers(TOKEN_CLASS_NUMBER)
        self.__match_emoticons(TOKEN_CLASS_EMOTICON)
        self.__match_repeated_chars(PUNCTUATION_MARKS__TERMINAL_POINTS, TOKEN_CLASS_PUNCTUATION_TERMINAL_POINTS_REPEATED)
        self.__match_repeated_chars(PUNCTUATION_MARKS__PAUSING_POINTS, TOKEN_CLASS_PUNCTUATION_PAUSING_POINTS_REPEATED)
        self.__match_puncuation_marks(PUNCTUATION_MARKS__TERMINAL_POINTS, TOKEN_CLASS_PUNCTUATION_TERMINAL_POINTS)
        self.__match_puncuation_marks(PUNCTUATION_MARKS__PAUSING_POINTS, TOKEN_CLASS_PUNCTUATION_PAUSING_POINTS)
        self.__match_alphanumeric_words(TOKEN_CLASS_ALPHANUM)
        self.__match_selected_characters('&', TOKEN_CLASS_ALPHANUM)
        self.__match_nonascii_characters(TOKEN_CLASS_NON_ASCII)
        self.__generate_token_list()


    def __match_html_entities(self, token_class):
        p = re.compile('&[^\s]*;')
        for m in p.finditer(self.__raw_string):
            self.__set_token_class(m.span()[0], m.span()[1], token_class)
            
    def __match_unicode_strings(self, token_class):
        p = re.compile('([\U])(\w+)\b')
        for m in p.finditer(self.__raw_string):
            self.__set_token_class(m.span()[0], m.span()[1], token_class)

    def __match_urls(self, token_class):
        #p = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        p = re.compile('https?://[^\s<>"]+|www\.[^\s<>"]+')
        for m in p.finditer(self.__raw_string):
            self.__set_token_class(m.span()[0], m.span()[1], token_class)
            
    def __match_emails(self, token_class):
        p = re.compile('([a-z0-9!#$%&\'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+\/=?^_`{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)')
        for m in p.finditer(self.__raw_string, re.UNICODE):
            self.__set_token_class(m.span()[0], m.span()[1], token_class)
            
    def __match_whitespaces(self, token_class):
        p = re.compile(' ')
        for m in p.finditer(self.__raw_string):
            self.__set_token_class(m.span()[0], m.span()[1], token_class)
            
    def __match_repeated_chars(self, character_list, token_class):
        for c1 in character_list:
            p = re.compile('['+c1+']{2,}')
            for m in p.finditer(self.__raw_string):
                self.__set_token_class(m.span()[0], m.span()[1], token_class)
                
    def __match_puncuation_marks(self, character_list, token_class):
        for c1 in character_list:
            p = re.compile('['+c1+']{1}')
            for m in p.finditer(self.__raw_string):
                self.__set_token_class(m.span()[0], m.span()[1], token_class)

    def __match_alphanumeric_words(self, token_class):
        p = re.compile('([a-zA-Z0-9])(?:[-[a-zA-Z0-9]|\']*([a-zA-Z0-9])?)?')
        #p = re.compile('({})(?:[-\w|\']*(\w)?)?')
        for m in p.finditer(self.__raw_string):
            self.__set_token_class(m.span()[0], m.span()[1], token_class)

    def __match_special_twitter_concepts(self, start_char, token_class):
        p = re.compile(start_char+'([A-Za-z_]+[A-Za-z0-9_]+)')
        for m in p.finditer(self.__raw_string):
            self.__set_token_class(m.span()[0], m.span()[1], token_class)


    def __match_numbers(self, token_class):
        p = re.compile('(?<=\s)[+-]?\d+(?:.\d)?\d*')
        for m in p.finditer(self.__raw_string):
            self.__set_token_class(m.span()[0], m.span()[1], token_class)

    def __match_emoticons(self, token_class):
        # Generic patterns 
        p = re.compile("[%s][%s]?[%s]+" % tuple(map(re.escape, [EMOTICONS_GENERIC_PATTERN_EYES, EMOTICONS_GENERIC_PATTERN_NOSES, EMOTICONS_GENERIC_PATTERN_MOUTHS])))
        for m in p.finditer(self.__raw_string):
            self.__set_token_class(m.span()[0], m.span()[1], token_class)
        # Generic patterns (mirrored orientation) 
        p = re.compile("[%s][%s]?[%s]+" % tuple(map(re.escape, [EMOTICONS_GENERIC_PATTERN_MOUTHS, EMOTICONS_GENERIC_PATTERN_NOSES, EMOTICONS_GENERIC_PATTERN_EYES])))
        for m in p.finditer(self.__raw_string):
            self.__set_token_class(m.span()[0], m.span()[1], token_class)

        # Fixed patterns
        p = re.compile('|'.join(map(re.escape, EMOTICONS_FIXED_PATTERNS)))
        for m in p.finditer(self.__raw_string):
            self.__set_token_class(m.span()[0], m.span()[1], token_class)

    
    def __match_nonascii_characters(self, token_class):
        p = re.compile("\W", re.UNICODE)
        for m in p.finditer(self.__raw_string):
            c1 = self.__raw_string[m.span()[0]:m.span()[1]]
            if c1 not in string.printable:
                self.__set_token_class(m.span()[0], m.span()[1], token_class)

    
    def __match_selected_characters(self, character_list, token_class):
        for c1 in character_list:
            p = re.compile('['+c1+']{1}')
            for m in p.finditer(self.__raw_string):
                self.__set_token_class(m.span()[0], m.span()[1], token_class)

    
    def __generate_token_list(self):
        self.__token_list = []
        token = ''
        token_class = -1
        for pos, val in enumerate(self.__char_map):
            if val != token_class or val == TOKEN_CLASS_NON_ASCII:
                if not token.isspace() and token_class >= 0:
                    self.__token_list.append((token, token_class, pos-len(token), len(token)))
                token = ''
                token_class = val
            token += self.__raw_string[pos]
            
        if token != '':
            self.__token_list.append((token, val, pos-len(token)+1, len(token)))
            
            
    def get_token_list(self):
        return self.__token_list
    
    def set_token_list(self, token_list):
        self.__token_list = token_list
    
    def get_urls(self):
        urls = []
        for token in self.__token_list:
            if token[1] in [TOKEN_CLASS_URL]:
                urls.append(token[0])
        return urls
            

    def generate_plain_tokens(self):
        tokens = []
        for token in self.__token_list:
            tokens.append(token[0])
        return tokens
    
    def generate_candidate_strings(self, valid_tokens, do_split=False):
        candidate_strings = []
        s = ''
        
        for token in self.__token_list:
            if token[1] in [TOKEN_CLASS_SPECIAL_TERM_TOPIC, TOKEN_CLASS_SPECIAL_TERM_USER]:
                if s != '':
                    candidate_strings.append(s.strip())
                s = ''
                candidate_strings.append(token[0].strip())
            elif token[1] in valid_tokens:
                if do_split == True:
                    candidate_strings.append(token[0])
                else:
                    s = s + token[0] + ' '
            else:
                if s != '':
                    candidate_strings.append(s.strip())
                s = ''
                 
        if s != '':
            candidate_strings.append(s.strip())
                
        return candidate_strings


    def generate_normalized_text(self, token_list=None, valid_token_list=None, convert_unicode=True, separator='|||'):
        s = ''
        phrase = ''
        for token in self.__token_list:
            if token[1] in valid_token_list:
                word = token[0]
                if token[1] == TOKEN_CLASS_NON_ASCII and convert_unicode == True:
                    word = word.encode('unicode-escape').upper()
                phrase += word + ' '
            else:
                if phrase != '':
                    s += phrase + separator + ' '
                    phrase = ''
        
        if phrase != '':
            s += phrase + separator + ' '
            
        return s[0:len(s)-(len(separator)+2)] # Remove the last character which are always ' | ' (if default separator)

    
    def generate_minimized_document(self, token_list=None, valid_token_list=None, convert_unicode=True):
        if token_list == None:
            token_list = self.__token_list
        punctuation_marks = [TOKEN_CLASS_PUNCTUATION_PAUSING_POINTS, TOKEN_CLASS_PUNCTUATION_PAUSING_POINTS_REPEATED, TOKEN_CLASS_PUNCTUATION_TERMINAL_POINTS, TOKEN_CLASS_PUNCTUATION_TERMINAL_POINTS_REPEATED]
        s = ''
        for token in token_list:
            if valid_token_list == None or token[1] in valid_token_list:
                word = token[0]
                if token[1] == TOKEN_CLASS_NON_ASCII and convert_unicode == True:
                    word = word.encode('unicode-escape').upper()
                if token[1] not in punctuation_marks: 
                    s += ' '
                s += word
        return s.strip()

    def generate_emoticon_list(self):
        emoticons = []
        for token in self.__token_list:
            if token[1] in [TOKEN_CLASS_EMOTICON]:
                emoticons.append(token[0])
        return emoticons
    
    
    def get_token_indexes(self, phrase, pos, offset, threshold):
        start = pos - threshold
        end = pos + offset + threshold - 1 - phrase.count(' ')
        token_indexes = []
    
        for index, token in enumerate(self.__token_list):
            if start <= token[2] <= end:
                token_indexes.append(index)
        return token_indexes  
    

if __name__ == "__main__":
    #ll = u'\\u0e4f\\u032f\\u0361\\u0e4f'.decode('unicode-escape')
    #print ll
    #print u'\\u0e4f\\u032f\\u0361\\u0e4f'.decode('unicode-escape')
    #s = '@JaeCreitch :-))) ..... ==>this ^^ is a real-world kidnapping .. Dr. Simpsons wonder what kind of passengers were on board....hmmmmmmm ----->http://t.co/DrYS8b4cZg'
    #s = ' You\'re Chinese satellite finds \'suspected crash site\' of Flight 370.01 http://t.co/5SlF1HPFe2 via @MailOnline #KIRUCODO'
    #s = 'START Season 2 @ , VivoCity at sd@MarinaBaySands #hungry'
    #s = 'Candlelight dinner with a #test candlelight Erm actually no candlelight #beanstro #marinabaysands http://t.co/UmNbxe3l18'.decode('unicode-escape')
    
    #print s
    se = "I\'m at Cafe 1 in Singapore https://t.co/E9ueFm7PLL"
    tokenizer = Tokenizer(se) 
    #print tokenizer.__raw_string
    print tokenizer.tokenize_as_tweet()
    print tokenizer.get_token_list()
    #print s
    #print tokenizer.get_token_list()
    #print tokenizer.generate_candidate_strings([TOKEN_CLASS_ALPHANUM, TOKEN_CLASS_IN_VOCABULARY_WORD, TOKEN_CLASS_IN_PLACE_VOCABULARY_WORD, TOKEN_CLASS_NUMBER, TOKEN_CLASS_SPECIAL_TERM_TOPIC, TOKEN_CLASS_SPECIAL_TERM_USER])
    
    #print tokenizer.generate_minimized_document(token_list=None, valid_token_list=[TOKEN_CLASS_ALPHANUM, TOKEN_CLASS_SPECIAL_TERM_TOPIC])
    