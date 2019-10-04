import newspaper
from newspaper import Article, Config
from newsplease import NewsPlease
from IPython.core.debugger import set_trace
from IPython.display import display
import extraction
import requests
import json
import os
import time
import hashlib
import glob
import pandas as pd
import news_publishers
from pathlib import Path
from langdetect import detect
from pubtime_extractor import extractArticlePublishedDate
import asyncio
from functools import partial

# Suppress UnknownTimezoneWarning
import warnings
from dateutil.parser import UnknownTimezoneWarning
warnings.filterwarnings('ignore', category=UnknownTimezoneWarning)


def _config():
    config = Config()
    config.fetch_images = False
    config.memoize_articles = False
    config.request_timeout = 10
    config.language = 'en'
    return config


def clean_url(pub, url):
    url = url.replace('http://', 'https://')

    try: url = url[:url.index('#')]
    except: pass

    try: url = url[:url.index('\n')]
    except: pass    
    
    if pub!='zdnet':
    # zdnet은 반드시 www가 붙어야되는 듯 (2019.08.30)
        url = url.replace('https://www.', 'https://')

    if pub=='axios':
        try: url = url[:url.index('?utm_source=')]
        except: pass
    
    if pub=='arstechnica':
        try: url = url[:url.index('?comments=1')]
        except: pass

    if pub=='americanconservative':
        try: url = url[:url.index('?print=1')]
        except: pass        
        
    if pub=='indiatimes':
        try: url = url[:url.index('?utm_source=')]
        except: pass      
        
    if pub=='reuters':
    # reuters는 뒤에 의미없이 ?il=0 이 붙는 경우가 허다. 무슨뜬인지는 모름 (2019.09.04)
        try: url = url[:url.index('?il=0')]
        except: pass
    
    if pub=='marketwatch':
        try: url = url[:url.index('?mod=')]
        except: pass
    
    if pub=='wsj':
    # wsj paywall 뚫기
        try: url = url[:url.index('?mod=')]
        except: pass
        
        url += '?mod=rsswn'
        
    if pub!='thinkprogress' and url[-1]=='/':
    # thinkprogress는 뒤의 /가 반드시 필요한 듯 (2019.09.04)
        url = url[:-1]    
        
    return url


class Progressor:
    def __init__(self, ntotal, formater_suffix=None):
        self.start = time.time()
        self.n_total = ntotal
        self.n_progressed = 0
        self.formater = '\r{pct:.2f}% ({timestamp:.2f} seconds)'

        if formater_suffix:
            self.formater += (': ' + formater_suffix)

    def stamp(self, **vargs):
        self.n_progressed += 1
        pct = self.n_progressed / self.n_total * 100
        timestamp = time.time() - self.start
        print(self.formater.format(pct=pct, timestamp=timestamp, **vargs), end='')
        

def collect_urls(src):
    prg = Progressor(len(src), formater_suffix='Collecting URLs... {pub:<20}')
    newspaper_config = partial(newspaper.build, config=_config())
        
    async def geturls(pub, *domains):
        urls = set()
        
        #if pub=='fox': set_trace()
        for domain in domains:
            resp = await loop.run_in_executor(None, newspaper_config, domain)
            urls |= {clean_url(pub, article.url) for article in resp.articles}

        prg.stamp(pub=pub)
        return pub, urls


    async def main():
        fts = [asyncio.ensure_future(geturls(pub, *val['domain'])) for pub, val in src.items()]
        return await asyncio.gather(*fts)


    result = None
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()

    try:
        # 다음 코드를 주피터에서 돌리려면, tornado를 downgrade 해야함
        # pip install tornado==4.5.3
        result = loop.run_until_complete(main())
        result = dict(result) #set.union(*result)

    except Exception as ex:
        print(ex)

    finally:
        loop.close()

    return result        
        


def get_publish_time(article):
    pubtime = article.publish_date
    url = article.url
    datesrc = 'newspaper'
    
    # articleDateExtractor 내부의 print 를 suppress 하기 위한 장치
    # --- articleDateExtractor 코드 자체를 변경함 (2019.09.05)
    #class HiddenPrints:
    #    def __enter__(self):
    #        self._original_stdout = sys.stdout
    #        sys.stdout = open(os.devnull, 'w')

    #    def __exit__(self, exc_type, exc_val, exc_tb):
    #        sys.stdout.close()
    #        sys.stdout = self._original_stdout
        
    
    def _from_extractor(url):
        try:
            return extractArticlePublishedDate(url)
        
        except:
            return None
    
    
    def _from_newsplease(url):
        try:
            return NewsPlease.from_url(url).date_publish
        
        except:
            return None
    
    
    def _timize(time):
        if time is None:
            return None
        
        try:
            time = pd.Timestamp(time)
            
            if time.tz is None:
                return time.tz_localize('utc')
            
            else:
                return time.tz_convert('utc')
        
        except:
            return None
        
    
    def _datize(time):
        if time is None:
            return ''

        try:
            time = pd.Timestamp(time)

            if time.tz is None:
                return str(time.date())

            else:
                return str(time.tz_convert('utc').date())
            
        except:
            return ''
            

    if pubtime is None:
        datesrc = 'extractor'
        pubtime = _from_extractor(url)

        if pubtime is None:
            datesrc = 'newsplease'
            pubtime = _from_newsplease(url)

            if pubtime is None:
                datesrc = 'fail'

    return _timize(pubtime)


# def fpath_of(hash_url, dirname_len=3):
#     ext = '.json'
#     return os.path.join(hash_url[dirname_len], hash_url + ext)


def select_urls(urls):
    prg = Progressor(len(urls), formater_suffix='Selecting URLs... {pub:<20}')
    selected = {}
    basedir = os.path.join(os.getcwd(), 'newsdata')
    ext = '.json'

    for pub, _urls in urls.items():
        selected[pub] = set()

        for _url in _urls:
            hash_url = hashlib.sha1(_url.encode('utf-8')).hexdigest()
            
            file_in_saved = os.path.join(basedir, 'saved', hash_url[:3], hash_url + ext)
            file_in_downloaded = os.path.join(basedir, 'downloaded', hash_url + ext)
            file_in_trashed = os.path.join(basedir, 'trashed', hash_url[:3], hash_url + ext)

            if os.path.isfile(file_in_saved) or os.path.isfile(file_in_downloaded) or os.path.isfile(file_in_trashed):
                continue
                
            else:
                selected[pub].add(_url)
                
        prg.stamp(pub=pub)
                
    return selected


def download(urls):
    n_total = sum([len(v) for _,v in urls.items()])
    prg = Progressor(n_total, formater_suffix='Downloading... {pub:<20}')
    basedir = os.path.join(os.getcwd(), 'newsdata')
    ext = '.json'
    newspaper_config = _config()
    
        
    def makedir_if_not_exists(file):
        _dir = os.path.dirname(file)
        
        if not os.path.isdir(_dir):
            os.makedirs(_dir)
            
            
    def detect_lang(article):
        lang = article.meta_lang
        
        if lang=='':
            return detect(article.text)
        
        else:
            return lang
            
    
    def get_article(url):
        article = Article(url, config=newspaper_config)
        article.download()
        article.parse()
        return article
        
        
    def get_title(article):
        if article.title in ['', '-', None]:
        # '':cbc, '-':townhall
            html = requests.get(article.url).text
            extracted_title = extraction.Extractor().extract(html, source_url=article.url).title
            
            if extracted_title in ['', '-', None]:
                if article.description=='':
                    return article.pub
                else:
                    return article.description
                
            else:
                return extracted_title
            
        else:
            return article.title


        
    async def _download(pub, _urls):
        out = {'downloaded':set(), 'trashed':set()}
        
        for url in _urls:
            hash_url = hashlib.sha1(url.encode('utf-8')).hexdigest()
            downloaded_at = pd.Timestamp.utcnow()
            is_downloaded = False
            
            content = {
                'pub': pub, 
                'url': url, 
                'downloaded_at': str(downloaded_at)
            }
            
            try: 
                article = await loop.run_in_executor(None, get_article, url)
                title = await loop.run_in_executor(None, get_title, article)
                content['title'] = title
                
                # 1. 텍스트가 없다면
                if article.text == '':
                    content['error'] = 'no text'

                else:
                    # 2. 텍스트가 너무 짧다면
                    if (not article.is_valid_body()) and (len(article.text)<500):
                        content['error'] = 'too short'
                
                    else:
                        language = detect_lang(article)
                        content['language'] = language
                        
                        # 3. 영어가 아니라면
                        if language != 'en':
                            content['error'] = 'not english'

                        else:
                            is_downloaded = True
                            published_at = await loop.run_in_executor(None, get_publish_time, article)

                            if published_at == None:
                                published_at = downloaded_at

                            content['text'] = article.text
                            content['description'] = article.meta_description
                            content['authors'] = article.authors
                            content['top_image'] = article.top_image if article.top_image.split('.')[-1]!='ico' else ''
                            content['published_at'] = str(published_at.date()) if published_at<=downloaded_at else str(downloaded_at.date())

            except:
                content['error'] = 'something wrong'


            if is_downloaded:
                file = os.path.join(basedir, 'downloaded', hash_url + ext)
                out['downloaded'].add(url)
                
            else:
                file = os.path.join(basedir, 'trashed', hash_url[:3], hash_url + ext)
                out['trashed'].add(url)
                
                
            makedir_if_not_exists(file)
            with open(file, 'w') as f:
                json.dump(content, f)
            
            
            # 종종 100%가 넘어가는 경우가 있다
            # set.union(*urls.values()) 에 중복항목이 있는 듯: 요건 set이라서 문제였던것 같다. 해결한듯 (2019.09.27)
            prg.stamp(pub=pub)
            
        return pub, out
    
        
    
    async def _download_old(pub, _urls):
        out = {'downloaded':set(), 'trashed':set()}
        
        for url in _urls:
            hash_url = hashlib.sha1(url.encode('utf-8')).hexdigest()
            downloaded_at = pd.Timestamp.utcnow()
            
            content = {
                'pub': pub, 
                'url': url, 
                'downloaded_at': str(downloaded_at)
            }
            
            try: 
                article = await loop.run_in_executor(None, get_article, url)
                title = await loop.run_in_executor(None, get_title, article)
                published_at = await loop.run_in_executor(None, get_publish_time, article)
                
                if published_at == None:
                    published_at = downloaded_at
                
                text = article.text
                language = detect_lang(article)
                is_too_short = (not article.is_valid_body()) and (len(article.text)<500)
                    
                content['published_at'] = str(published_at.date()) if published_at<=downloaded_at else str(downloaded_at.date())
                content['title'] = title
                content['language'] = language
                
                if text == '':
                    file = os.path.join(basedir, 'trashed', hash_url[:3], hash_url + ext)
                    content['error'] = 'no text'
                    out['trashed'].add(url)
                    
                elif is_too_short:
                    file = os.path.join(basedir, 'trashed', hash_url[:3], hash_url + ext)
                    content['error'] = 'too short'
                    out['trashed'].add(url)
                    
                elif language != 'en':
                    file = os.path.join(basedir, 'trashed', hash_url[:3], hash_url + ext)
                    content['error'] = 'not english'
                    out['trashed'].add(url)

                else:
                    file = os.path.join(basedir, 'downloaded', hash_url + ext)
                    content['text'] = text
                    content['description'] = article.meta_description
                    content['authors'] = article.authors
                    content['top_image'] = article.top_image if article.top_image.split('.')[-1]!='ico' else ''
                    out['downloaded'].add(url)
            
            except:
                file = os.path.join(basedir, 'trashed', hash_url[:3], hash_url + ext)
                content['error'] = 'something wrong'
                out['trashed'].add(url)
            
            
            makedir_if_not_exists(file)
            with open(file, 'w') as f:
                json.dump(content, f)
            
            prg.stamp(pub=pub)
            
        return pub, out


    async def main():
        fts = [asyncio.ensure_future(_download(pub, _urls)) for pub, _urls in urls.items()]
        return await asyncio.gather(*fts)

    
    result = None
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()

    try:
        result = loop.run_until_complete(main())
        result = dict(result)

    except Exception as ex:
        print(ex)

    finally:
        loop.close()
        
    return result



def download2(urls):
    n_total = sum([len(v) for _,v in urls.items()])
    prg = Progressor(n_total, formater_suffix='downloading... {pub:<20}')
    basedir = os.path.join(os.getcwd(), 'newsdata')
    ext = '.json'
    newspaper_config = _config()
    
        
    def makedir_if_not_exists(file):
        _dir = os.path.dirname(file)
        
        if not os.path.isdir(_dir):
            os.makedirs(_dir)
            
            
    def detect_lang(article):
        lang = article.meta_lang
        
        if lang=='':
            return detect(article.text)
        
        else:
            return lang
            
    
    def get_article(url):
        article = Article(url, config=newspaper_config)
        article.download()
        article.parse()
        return article
        
        
    def get_title(article):
        if article.title in ['', '-', None]:
        # '':cbc, '-':townhall
            html = requests.get(article.url).text
            extracted_title = extraction.Extractor().extract(html, source_url=article.url).title
            
            if extracted_title in ['', '-', None]:
                if article.description=='':
                    return article.pub
                else:
                    return article.description
                
            else:
                return extracted_title
            
        else:
            return article.title
        
    
    async def _download(pub, _urls):
        out = {'downloaded':set(), 'trashed':set()}
        
        for url in _urls:
            is_downloaded = False
            hash_url = hashlib.sha1(url.encode('utf-8')).hexdigest()
            #downloaded_at = pd.Timestamp.utcnow()

            #########################
            trashed_file = os.path.join(basedir, 'trashed', hash_url[:3], hash_url + ext)
            js = json.loads(Path(trashed_file).read_text())
            downloaded_at = pd.Timestamp(js['downloaded_at'])
                
            url = clean_url(pub, url)
            hash_url = hashlib.sha1(url.encode('utf-8')).hexdigest()
            #########################
            
            content = {
                'pub': pub, 
                'url': url, 
                'downloaded_at': str(downloaded_at)
            }
            
            try: 
                article = await loop.run_in_executor(None, get_article, url)
                title = await loop.run_in_executor(None, get_title, article)
                content['title'] = title
                
                # 1. 텍스트가 없다면
                if article.text == '':
                    content['error'] = 'no text'

                else:
                    # 2. 텍스트가 너무 짧다면
                    if (not article.is_valid_body()) and (len(article.text)<500):
                        content['error'] = 'too short'
                
                    else:
                        language = detect_lang(article)
                        content['language'] = language
                        
                        # 3. 영어가 아니라면
                        if language != 'en':
                            content['error'] = 'not english'

                        else:
                            is_downloaded = True
                            published_at = await loop.run_in_executor(None, get_publish_time, article)

                            if published_at == None:
                                published_at = downloaded_at

                            content['text'] = article.text
                            content['description'] = article.meta_description
                            content['authors'] = article.authors
                            content['top_image'] = article.top_image if article.top_image.split('.')[-1]!='ico' else ''
                            content['published_at'] = str(published_at.date()) if published_at<=downloaded_at else str(downloaded_at.date())

            except:
                content['error'] = 'something wrong'


            if is_downloaded:
                file = os.path.join(basedir, 'downloaded', hash_url + ext)
                out['downloaded'].add(url)
                Path(trashed_file).unlink()
                
            else:
                file = os.path.join(basedir, 'trashed', hash_url[:3], hash_url + ext)
                out['trashed'].add(url)
                
                
            makedir_if_not_exists(file)
            with open(file, 'w') as f:
                json.dump(content, f)
            
                
            # 종종 100%가 넘어가는 경우가 있다
            # set.union(*urls.values()) 에 중복항목이 있는 듯: 요건 set이라서 문제였던것 같다. 해결한듯 (2019.09.27)
            prg.stamp(pub=pub)
            
        return pub, out


    async def main():
        fts = [asyncio.ensure_future(_download(pub, _urls)) for pub, _urls in urls.items()]
        return await asyncio.gather(*fts)

    
    result = None
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()

    try:
        result = loop.run_until_complete(main())
        result = dict(result)

    except Exception as ex:
        #pass
        print(ex)

    finally:
        loop.close()
        
    return result



class NewsCrawler:
    def __init__(self, *pubs):
        if len(pubs) == 0:
            self.src = news_publishers.src
            
        else:
            self.src = {k:v for k,v in news_publishers.src.items() if k in pubs}
            

    def collect(self):
        '''
        collecting 과정에서 pub간에 겹치는 url이 있을 수 있다
        따라서 urls의 총 갯수와 UNION(urls)의 갯수는 다를 수 있다
        이는 아래 selecting도 마찬가지 (2019.09.27)
        '''
        self.urls_collected = collect_urls(self.src)
        return self._results_sub(self.urls_collected)

        
    def select(self):
        self.urls_selected = select_urls(self.urls_collected)
        return self._results_sub(self.urls_selected)
    
    
    def download(self):
        '''
        collecting, selecting 과정에서 pub간의 겹치는 url이 있었으나, 
        download된 파일명은 url의 hashcode이므로, 모든 파일은 유니크한 url만 담고있다
        async download 과정에서, 나중에 받아진 내용으로 이전 파일을 덮어쓴다 (2019.09.27)
        '''
        self.urls_final = download(self.urls_selected)
        return self._results_final(self.urls_final)

    
    def download2(self):
        self.urls_final = download2(self.urls_selected)
        return self._results_final(self.urls_final)    
    
        
    def _summary_by_pubs(self, urls):
        return pd.Series({pub:len(_urls) for pub, _urls in urls.items()})
    
    
    def _uniquenese(self, urls):
        urls_list = sum([list(v) for _,v in urls.items()], [])
        n_total = len(urls_list)
        n_unique = len(set(urls_list))
        return pd.Series({'n_total':n_total, 'n_unique':n_unique})

    
    def _duplicates(self, urls):
        urls_tmp = {k:{_v:1 for _v in v} for k,v in urls.items()}
        df_dupl = pd.DataFrame.from_dict(urls_tmp, orient='columns')
        df_dupl = df_dupl[df_dupl.sum(axis=1)!=1]
        cols = df_dupl.columns

        duplicates = {}
        for url, row in df_dupl.iterrows():
            pubs = cols[row==1]
            actual_pub = pubs[0]

            for pub in pubs:
                if pub in url:
                    actual_pub = pub
                    break

            duplicates[url] = [', '.join(pubs), actual_pub]

        return pd.DataFrame.from_dict(duplicates, orient='index', columns=['pubs', 'actual_pub'])
    
    
    def _results_sub(self, urls):
        uniqueness = self._uniquenese(urls)
        summary_by_pubs = self._summary_by_pubs(urls)        
        duplicates = self._duplicates(urls)
        return uniqueness, summary_by_pubs, duplicates
    
    
    def _results_final(self, urls_final):
        tmp = {pub:{state:len(_urls) for state, _urls in urls.items()} for pub,urls in urls_final.items()}
        return pd.DataFrame.from_dict(tmp, orient='index')