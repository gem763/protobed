import re
from spacy.pipeline import EntityRuler
import gensim


class MergedTokenizer:
    def __init__(self, nlp, merge_ner=True, merge_chunks=False, allowed_pos=None):
        self.nlp = self._nlp_pipe_added(nlp)
        self.merge_ner = merge_ner
        self.merge_chunks = merge_chunks
        self.allowed_pos = ['NOUN','ADJ','VERB','ADV','NUM','PROPN'] if allowed_pos is None else allowed_pos

        
    def __call__(self, rawtext):
        return self._tokenize(rawtext)

    
    def _tokenize(self, rawtext):
        '''spacy의 token 객체를 넘긴다(str이 아님)'''
        doc = self.nlp(self._preprocess(rawtext))
        self._merge(doc)            
        return self._postprocess(doc)    
    
    
    def lemmatized(self, rawtext, lower=True):
        '''lemmatized된 str을 넘긴다'''
        tokens = self(rawtext)
        
        if lower:
            return [tok.lemma_.lower() for tok in tokens]
        else:
            return [tok.lemma_ for tok in tokens]
    
    
    def _nlp_pipe_added(self, nlp):
        ruler = EntityRuler(nlp)
        patterns = [
            {"label": "MONEY", "pattern": [{"TEXT": "$"}, {"POS": "NUM"}]},
            {"label": "MONEY", "pattern": [{"TEXT": "€"}, {"POS": "NUM"}]},
            {"label": "MONEY", "pattern": [{"TEXT": "¥"}, {"POS": "NUM"}]},
            {"label": "MONEY", "pattern": [{"TEXT": "£"}, {"POS": "NUM"}]},
        #     {"label": "MONEY", "pattern": [{"TEXT": {"REGEX": r"[\$|€|¥|£]"}}, {"POS": "NUM"}]} #원화\ 는 잘 안된다...
        ]
        
        ruler.add_patterns(patterns)

        if nlp.has_pipe('entity_ruler'):
            nlp.replace_pipe('entity_ruler', ruler)

        else:
            nlp.add_pipe(ruler, before='ner')
            
        return nlp
    
    
    def _preprocess(self, rawtext):
        rawtext = re.sub(r'\n+', r'\n', rawtext)
        rawtext = gensim.utils.simple_preprocess(rawtext, deacc=True)
        return ' '.join(rawtext)
    
    
    def _postprocess(self, doc):
        return [tok for tok in doc if self._is_allowed(tok)]
    
    
    def _merge(self, doc):
        spans = []
        
        if self.merge_ner:
            spans.extend(doc.ents)
            
        if self.merge_chunks:
            for nc in doc.noun_chunks:        
                while len(nc)>1 and nc[0].dep_ not in ('advmod', 'amod', 'compound', 'nummod'):
                    nc = nc[1:]
                spans.append(nc)
                
        if self.merge_ner and self.merge_chunks:
            spans = self._filter_spans(spans)
            
        with doc.retokenize() as retokenizer:
            for span in spans:
                root = span.root
                # entity인 2%의 lemma가 2 %가 되기 때문에, 이경우 2-%가 된다. 
                # 이런 경우를 제외하기 위해, 그냥 span.text를 썼다 (2019.09.17)
                lemma = span.text.replace(' ', '_') if len(span)>1 else span.lemma_
                attrs = {'tag':root.tag_, 'lemma':lemma, 'ent_type':root.ent_type_}
                retokenizer.merge(span, attrs=attrs)

    
    def _is_allowed(self, tok):
        if tok.is_stop or tok.is_punct or tok.is_space or (tok.pos_ not in self.allowed_pos):
            return False
        else:
            return True
        
        
    def _filter_spans(self, spans):
        get_sort_key = lambda span: (span.end - span.start, span.start)
        sorted_spans = sorted(spans, key=get_sort_key, reverse=True)
        result = []
        seen_tokens = set()

        for span in sorted_spans:
            if span.start not in seen_tokens and span.end -1 not in seen_tokens:
                result.append(span)
                seen_tokens.update(range(span.start, span.end))

        return result