import re
import nltk

def remove_last_word(string):
    """
    Takes in a string.
    Splits the string into a list of words.
    Removes the last word from the list.
    Returns the list as a string.
    """

    words = string.split()
    if len(words) > 1:
      words.pop()
    else:
      words = words
    return ' '.join(words)

def utils_preprocess_text(text, flg_stemm=False, flg_lemm=True, lst_stopwords=None):
    ## clean (convert to lowercase and remove punctuations and   characters and then strip)
    text = re.sub(r'[^\w\s]', '', str(text).strip())
            
    ## Tokenize (convert from string to list)
    lst_text = text.split()
    ## remove Stopwords
    if lst_stopwords is not None:
        lst_text = [word for word in lst_text if word not in 
                    lst_stopwords]
                
    ## Stemming (remove -ing, -ly, ...)
    if flg_stemm == True:
        ps = nltk.stem.porter.PorterStemmer()
        lst_text = [ps.stem(word) for word in lst_text]
                
            
    ## back to string from list
    text = " ".join(lst_text)
    return text
  
def change_none_to_string(df, column, string):
    """
    Takes in a dataframe, a column, and a string.
    Changes all None values in the column to the given string.
    """
    df[column] = df[column].apply(lambda x: string if x is None else x)
    return df


def findKeyword(df, column, keyword,keyword_cotains:bool):
    """ a function that finds non keyword values in a column, column must be str and keyword must be str"""
    if keyword_cotains:
        return (df[df[column].str.contains(keyword)]).reset_index(drop=True)
    else:
         return (df[~df[column].str.contains(keyword)]).reset_index(drop=True)

 
def find_exact_match(df1, col1, col2):
    """
    a function that takes two columns containing strings in one dataframe
    lowers each string in each column
    find exact matches
    and returns a dataframe with the matching indexes
    
     """
    df = df1.copy(deep=True)
    df[col1] = df[col1].str.lower()
    df[col2] = df[col2].str.lower()
    df['match'] = df[col1] == df[col2]
    df_match = df1[df['match'] == True]
    return df_match
  
def findnonNAinColumn(df, column):
    """ a function that finds non NA values in a column"""
    return (df[~df[column].isnull()]).reset_index(drop=True)
  
def findNAinColumn(df, column):
    """ a function that finds non NA values in a column"""
    return (df[df[column].isnull()]).reset_index(drop=True)


def splitString(string):
    """ a function that splits a string into a list of words"""
    return string.split()