'''
src의 key는 domain에 포함되어 있는 글자로 한다
select_urls()에서 url의 중복을 체크하기 위해 (2019.10.04)
'''

src = {
             'huffpost': {'pubname': 'HuffPost',                    'domain': ['https://huffpost.com']}, 
                  'cnn': {'pubname': 'CNN',                         'domain': ['https://cnn.com']}, # ?=
        'investing.com': {'pubname': 'Investing.com',               'domain': ['https://investing.com']}, 
             'politico': {'pubname': 'POLITICO',                    'domain': ['https://politico.com']}, 
                 'time': {'pubname': 'TIME',                        'domain': ['https://time.com']}, 
                 'cnbc': {'pubname': 'CNBC',                        'domain': ['https://cnbc.com']}, 
                  'fox': {'pubname': 'FOX',                         'domain': ['https://foxnews.com', 'https://foxbusiness.com']}, 
                  'bbc': {'pubname': 'BBC',                         'domain': ['https://bbc.com']}, 
      'businessinsider': {'pubname': 'Business Insider',            'domain': ['https://businessinsider.com']}, 

          'morningstar': {'pubname': 'Morningstar',                 'domain': ['https://morningstar.com']}, 
                  'wsj': {'pubname': 'Wall Street Journal',         'domain': ['https://wsj.com']}, # ?mod=rsswn
              'nytimes': {'pubname': 'NewYork Times',               'domain': ['https://nytimes.com']}, 
             'guardian': {'pubname': 'Guardian',                    'domain': ['https://theguardian.com']}, 
              'reuters': {'pubname': 'Reuters',                     'domain': ['https://reuters.com']}, # ?=불필요, 심각
      'washingtontimes': {'pubname': 'Washington Times',            'domain': ['https://washingtontimes.com']}, 
       'washingtonpost': {'pubname': 'Washington Post',             'domain': ['https://washingtonpost.com']}, # ?=
                  'cbs': {'pubname': 'CBS',                         'domain': ['https://cbsnews.com']}, 
          'marketwatch': {'pubname': 'MarketWatch',                 'domain': ['https://marketwatch.com']}, # ?= 심각
             'atlantic': {'pubname': 'Atlantic',                    'domain': ['https://theatlantic.com']}, 

                 'vice': {'pubname': 'VICE',                        'domain': ['https://www.vice.com/en_us']}, 
                  'npr': {'pubname': 'npr',                         'domain': ['https://npr.org']}, 
          'newrepublic': {'pubname': 'NEW REPUBLIC',                'domain': ['https://newrepublic.com']}, 
                'yahoo': {'pubname': 'yahoo',                       'domain': ['https://yahoo.com', 'https://news.yahoo.com']}, 
          'independent': {'pubname': 'INDEPENDENT',                 'domain': ['https://independent.co.uk']}, 
             'heritage': {'pubname': 'Heritage',                    'domain': ['https://heritage.org']}, 
                'zdnet': {'pubname': 'ZDNet',                       'domain': ['https://www.zdnet.com']}, # 반드시 www가 붙어야함
             'townhall': {'pubname': 'Townhall',                    'domain': ['https://townhall.com']}, 
              'abcnews': {'pubname': 'ABC News',                    'domain': ['https://abcnews.go.com']}, # ?=많긴한데 반드시필요
               'hotair': {'pubname': 'HOT AIR',                     'domain': ['https://hotair.com']}, 
    
                  'cbc': {'pubname': 'CBC',                         'domain': ['https://cbc.ca']}, 
                'nymag': {'pubname': 'NewYork Magazine',            'domain': ['https://nymag.com']}, 
            'thestreet': {'pubname': 'TheStreet',                   'domain': ['https://www.thestreet.com']}, # 반드시 www가 붙어야함 
        'thinkprogress': {'pubname': 'ThinkProgress',               'domain': ['https://thinkprogress.org']}, 
           'dailybeast': {'pubname': 'DAILY BEAST',                 'domain': ['https://thedailybeast.com']}, 
    'realclearpolitics': {'pubname': 'RealClear Politics',          'domain': ['https://www.realclearpolitics.com']}, # 반드시 www가 붙어야함
            'aljazeera': {'pubname': 'Al Jazeera',                  'domain': ['https://aljazeera.com']}, 
    
              'arynews': {'pubname': 'ARYNEWS',                     'domain': ['https://arynews.tv/en']}, 
                  'afr': {'pubname': 'Australian Financial Review', 'domain': ['https://afr.com']}, 
                'axios': {'pubname': 'AXIOS',                       'domain': ['https://axios.com']}, # ?utm_source=

         'blastingnews': {'pubname': 'Blastingnews',                'domain': ['https://us.blastingnews.com']}, 
            'breitbart': {'pubname': 'BREITBART',                   'domain': ['https://breitbart.com']}, 
            'dailymail': {'pubname': 'Daily Mail',                  'domain': ['https://dailymail.co.uk']}, 
        'financialpost': {'pubname': 'Financial Post',              'domain': ['https://business.financialpost.com']}, 
                'metro': {'pubname': 'METRO',                       'domain': ['https://metro.co.uk']}, 
                'msnbc': {'pubname': 'MSNBC',                       'domain': ['https://msnbc.com']}, 
       'nationalreview': {'pubname': 'NATIONAL REVIEW',             'domain': ['https://nationalreview.com']}, 
               'news24': {'pubname': 'News24',                      'domain': ['https://news24.com']}, 
           'techcrunch': {'pubname': 'TechCrunch',                  'domain': ['https://techcrunch.com']}, 
          'arstechnica': {'pubname': 'Ars TECHNICA',                'domain': ['https://arstechnica.com']}, # ?comments=1

             'euronews': {'pubname': 'euronews',                    'domain': ['https://euronews.com']}, 
               'mirror': {'pubname': 'Mirror',                      'domain': ['https://mirror.co.uk']}, 
              'nbcnews': {'pubname': 'NBC News',                    'domain': ['https://nbcnews.com']}, 
          'news.com.au': {'pubname': 'news.com.au',                 'domain': ['https://news.com.au']}, 
        'nextbigfuture': {'pubname': 'NextBigFuture',               'domain': ['https://nextbigfuture.com']}, 
                   'rt': {'pubname': 'RT',                          'domain': ['https://rt.com']}, 
 'americanconservative': {'pubname': 'American Conservative',       'domain': ['https://theamericanconservative.com']}, # ?print=1
              'thehill': {'pubname': 'TheHill',                     'domain': ['https://thehill.com']}, 
           'thenextweb': {'pubname': 'TNW',                         'domain': ['https://thenextweb.com']}, 
            'telegraph': {'pubname': 'The Telegraph',               'domain': ['https://telegraph.co.uk']}, 

           'indiatimes': {'pubname': 'THE TIMES OF INDIA',          'domain': ['https://timesofindia.indiatimes.com']}, # ?utm_source=
             'theverge': {'pubname': 'THE VERGE',                   'domain': ['https://theverge.com']}, 
             'usatoday': {'pubname': 'USA TODAY',                   'domain': ['https://usatoday.com']}, 
           'chinadaily': {'pubname': 'CHINADAILY',                  'domain': ['https://global.chinadaily.com.cn']}, 
                 'scmp': {'pubname': 'South China Morning Post',    'domain': ['https://scmp.com']}, 
           'japan-news': {'pubname': 'The Japan News',              'domain': ['https://the-japan-news.com']}, 
           'japantoday': {'pubname': 'JAPANTODAY',                  'domain': ['https://japantoday.com']}, 
               'chosun': {'pubname': 'CHOSUN',                      'domain': ['https://english.chosun.com']}, 
             'joongang': {'pubname': 'Joongang Daily',              'domain': ['https://koreajoongangdaily.joins.com']}, 
              'arirang': {'pubname': 'arirang',                     'domain': ['https://arirang.com']}, 

                  'ccn': {'pubname': 'CCN',                         'domain': ['https://ccn.com']}, 
        'cointelegraph': {'pubname': 'COINTELEGRAPH',               'domain': ['https://cointelegraph.com']}, 
           'cryptocoin': {'pubname': 'CryptoCoin.News',             'domain': ['https://cryptocoin.news']}, 
           'cryptonews': {'pubname': 'cryptonews',                  'domain': ['https://cryptonews.com']}, 
    
    #'forbes':          'https://forbes.com', 
    #'hbr':             'https://hbr.org', 
    #'ft':              'https://ft.com', 
    #'economist':       'https://economist.com', 
}