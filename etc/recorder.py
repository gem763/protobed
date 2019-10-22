import pandas as pd
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

localpath_to_downloaded = 'newsdata/downloaded'
localpath_to_trashed = 'newsdata/trashed'


class Recorder:
    def __init__(self, storage='local'):
        self.storage = storage
        self.ids = self._get_ids(storage)

    def _query_ids_from_bigquery(self, tb):
        qry = 'SELECT id FROM `{}`'.format(proj + '.' + tb)
        return gbq.read_gbq(qry, credentials=credentials).id
        
    def _retreive_ids_from_local(self, path):
        return [p.stem for p in Path(path).glob('**/*.json')]
        
        
    def _get_ids(self, storage):
        print('checking ' + storage + ' storage... ', end='')

        if storage == 'bigquery':
            ids_downloaded = self._query_ids_from_bigquery(table_downloaded)
            ids_trashed = self._query_ids_from_bigquery(table_trashed)

        elif storage == 'local':
            ids_downloaded = self._retreive_ids_from_local(localpath_to_downloaded)
            ids_trashed = self._retreive_ids_from_local(localpath_to_trashed)

        ids_downloaded_set = set(ids_downloaded)
        ids_trashed_set = set(ids_trashed)
        
        if len(ids_downloaded) != len(ids_downloaded_set):
            '''downloaded articles의 uniqueness'''
            raise self.DuplicatesInSingleTable('duplicated in downloaded')

        if len(ids_trashed) != len(ids_trashed_set):
            '''trashed articles의 uniqueness'''
            raise self.DuplicatesInSingleTable('duplicated in trashed')

        if len(ids_downloaded_set & ids_trashed_set) != 0:
            '''downloaded와 trashed 간의 uniqueness'''
            raise self.DuplicatesBetweenTwoTables('duplicated between downloaded and trashed')
    
        ids = ids_downloaded_set | ids_trashed_set
        
        print('done')
        print('we have total {} ({} downloaded, {} trashed)'.format(len(ids), len(ids_downloaded_set), len(ids_trashed_set)))
        return ids


    def has(self, id):
        return id in self.ids


    def update(self, list_downloaded=None, list_trashed=None, chunksize=1000, subdir_len=3):
        if self.storage == 'bigquery':
            self._update_bigquery('downloaded', list_downloaded, chunksize)
            self._update_bigquery('trashed', list_trashed, chunksize)
        
        elif self.storage == 'local':
            self._update_local('downloaded', list_downloaded, subdir_len)
            self._update_local('trashed', list_trashed, subdir_len)
            
            
    def _update_local(self, newstype, newslist, subdir_len):
        if newslist is not None:
            if newstype == 'downloaded':
                path = localpath_to_downloaded
            elif newstype == 'trashed':
                path = localpath_to_trashed
            
            for article in newslist:
                id = article.pop('id')
                _dir = Path(path + '/' + id[:subdir_len])
                _dir.mkdir(parent=True, exist_ok=True)
                fname = id + '.json'
                fpath = _dir / fname
                with fpath.open('w') as f:
                    json.dump(article)
                    
            
    def _update_bigquery(self, newstype, newslist, chunksize):
        if newslist is not None:
            if newstype == 'downloaded':
                tb = table_downloaded
            elif newstype == 'trashed':
                tb = table_trashed

            df = pd.DataFrame(newslist)
            gbq.to_gbq(df, tb, project_id=proj, if_exists='append', chunksize=chunksize, credentials=credentials)



    class DuplicatesInSingleTable(Exception):
        pass

    class DuplicatesBetweenTwoTables(Exception):
        pass