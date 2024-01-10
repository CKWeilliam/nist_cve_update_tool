from lib.nvd_cve_updater import CveUpdater
from lib.nvd_cve_tool import NvdCveDownloader

'''
This is a funtion that can get the latest CVE data from NVD.
'''

url = 'https://services.nvd.nist.gov/rest/json/cves/2.0'
api_key = {'apiKey':'e57078be-2f1a-498e-a98e-342f21ed98aa'}
cve_updater = CveUpdater()
nvd_cve_downloader = NvdCveDownloader(url, api_key)

# Read local cve json data
cve_web_data = CveUpdater().web_data_json()

# upload cve data form NVD
# cve_web_data = nvd_cve_downloader.get_all_nvd_web_data(url, api_key)
cve_updater.nvd_cve_update_and_insert(cve_web_data)
