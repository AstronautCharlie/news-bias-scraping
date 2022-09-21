"""
Defines functionality used for headline analysis 
"""
import pandas as pd 
import spacy 
import datetime
SPACY_MODEL = 'en_core_web_sm'
nlp = spacy.load(SPACY_MODEL)


'''
class headline_analyzer:
    def __init__(self, df, spacy_model='en_core_web_sm'):
        # Takes in pandas df, optionally the spacy model 
        self.df = df 
        self.nlp = spacy.load(spacy_model)

    # -----------------
    # Utility functions  
    # -----------------
'''

def extract_nouns_entities(row): 
    """
    Extract all nouns and entities from the headline sections of the row 
    """
    nouns = [] 
    entities = [] 
    headline = nlp(row.headline)

    # Get nouns
    for token in headline:
        if token.pos_ in ['PROPN', 'NOUN']:
            nouns.append(token)

    # Get entities
    for ent in headline.ents:
        entities.append(ent)

    row['nouns'] = nouns 
    row['entities'] = entities
    return row 

def reverse_count_dict(dic, reverse=True):
    """
    Reverse a dictionary {k->v} and return {v->Set(k s.t. dic[k]==v)}
    
    k is a count, and v is the set of items with that count. 

    sort dictionary descending by default 
    """
    results = {} 
    for k, v in dic.items(): 
        if v in results.keys(): 
            results[v].add(k)
        else: 
            results[v] = {k}
    items = results.items()
    return sorted(items, reverse=reverse)

def get_percent_count(dic):
    """
    Given a count dictionary, return a new dictionary with percent of 
    total counts instead of raw count 
    """
    total = sum([v[0] for v in dic])

    results = {} 
    for k, v in dic: 
        results[k / total] = v
    return results 

# ------------------
# Analysis Functions
# ------------------

def count_nouns_entities(df, start_date=None, end_date=None):
    """
    Count all the nouns and entities in the df, return two dicts 
    of {noun/entity->count} 

    dates must be YYYY-MM-DD
    """
    nouns = {} 
    entities = {} 

    for i, r in df.iterrows(): 
        if start_date and r['start_date'] < start_date: 
            continue 
        if end_date and r['end_date'] > end_date: 
            continue 
        else: 
            for n in r['nouns']: 
                n_s = str(n)
                if n_s in nouns.keys(): 
                    nouns[n_s] += 1 
                else: 
                    nouns[n_s] = 1
            for e in r['entities']:
                e_s = str(e)
                if e_s in entities.keys(): 
                    entities[e_s] += 1 
                else: 
                    entities[e_s] = 1 

    return nouns, entities

def count_nouns(df, start_date=None, end_date=None): 
    nouns, _ = count_nouns_entities(df, start_date=start_date, end_date=end_date)
    return nouns 

def count_entities(df, start_date=None, end_date=None):
    _, entities = count_nouns_entities(df, start_date=start_date, end_date=end_date)
    return entities


# --------------------
# Production Functions 
# --------------------

