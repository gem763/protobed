import pandas_gbq as gbq
from google.oauth2 import service_account
from IPython.core.debugger import set_trace

'''
Configuration
'''
proj = 'global-news-crawl'
table_downloaded = 'news_dataset.downloaded'
table_trashed = 'news_dataset.trashed'
credentials = service_account.Credentials.from_service_account_file('global-news-crawl-c48d7cd9aa81.json')


class BigqueryLoader:
    def __init__(self):
        self.ids = self._get_ids()
    
    def _get_ids(self):
        print('checking bigqueryloader status... ', end='')
        
        qry_ids = lambda prj, tb: 'SELECT id FROM `{}`'.format(prj + '.' + tb)
        qry_downloaded = qry_ids(proj, table_downloaded)
        qry_trashed = qry_ids(proj, table_trashed)
        
        ids_downloaded = gbq.read_gbq(qry_downloaded, project_id=proj, credentials=credentials)
        ids_trashed = gbq.read_gbq(qry_trashed, project_id=proj, credentials=credentials)
        
        ids_downloaded_set = set(ids_downloaded.id)
        ids_trashed_set = set(ids_trashed.id)
        
        if len(ids_downloaded) != len(ids_downloaded_set):
            raise self.DuplicatesInSingleTable('duplicated in downloaded')

        if len(ids_trashed) != len(ids_trashed_set):
            raise self.DuplicatesInSingleTable('duplicated in trashed')

        if len(ids_downloaded_set & ids_trashed_set) != 0:
            raise self.DuplicatesBetweenTwoTables('duplicated between downloaded and trashed')
    
        ids = ids_downloaded_set | ids_trashed_set
        
        print('done')
        print('we have total {} ids ({} downloaded, {} trashed)'.format(len(ids), len(ids_downloaded_set), len(ids_trashed_set)))
        return ids
        
        
    def has(self, id):
        return id in self.ids
        
    def upload(self, df, to, chunksize=1000):
        gbq.to_gbq(df, to, project_id=proj, if_exists='append', chunksize=chunksize, credentials=credentials)
        
    class DuplicatesInSingleTable(Exception):
        pass
    
    class DuplicatesBetweenTwoTables(Exception):
        pass