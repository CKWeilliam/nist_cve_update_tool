from database.mongo_db import KB
from lib.nvd_cve_updater import CveUpdater

'''
This funtion can reset the database directly, 
but "nvdCveUploader\nvdOutput\nvdOutput.json" must already exist.
'''

knowledge_base = KB()
cve_updater = CveUpdater()
db_name = 'kb'
collection_name = 'nvd_lst'

# delete all data in data base
knowledge_base.delete_all_data(db_name, collection_name)

# insert new data from laocal Json
data = cve_updater.web_data_json()
knowledge_base = KB()
batch_size = 10000  # Setting the batch for each insert
knowledge_base.insert_many_data(db_name, collection_name, data, batch_size)