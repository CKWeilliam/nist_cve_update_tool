import json
import requests
import typing
import time
import os


class NvdCveDownloader():
    '''
    A library for processing data retrieved from the Database (NVD).
    It includes functionality for handling URI iteration, data structure 
    transformation, and backing up data locally.

    '''
    def __init__(self, url, header) -> None:
        self.url = url
        self.header = header
        self.request_cd = time.sleep(0)  # without key need to change to 7sec
        self.result_batch = 2000

    def get_total_results(self) -> int:
        """
        Fetches the total number of results available in the NVD.

        Returns:
            int: Total number of results in the NVD.
        """
        res = requests.get(self.url)
        res_dict = json.loads(res.text)
        total_results_number = res_dict["totalResults"]

        return int(total_results_number)

    def url_generator(self) -> list:
        """
        Generates a list of URLs for fetching NVD data in batches.

        Returns:
            list: List of URLs for NVD data retrieval.
        """
        url_list = []
        total_number = self.get_total_results()
        batch_number = total_number // self.result_batch
        for i in range(batch_number + 1):
            url_list.append(
                f'{self.url}/?resultsPerPage={self.result_batch}&startIndex={i * self.result_batch}')

        return url_list

    def reformat_nvd_dict_to_list(self, res_dict) -> typing.List[dict]:
        """
        Transforms the NVD data dictionary into a list of reformatted 
        dictionaries.

        Args:
            res_dict (dict): NVD data dictionary.

        Returns:
            list: List of reformatted dictionaries.
        """
        new_res_dict_lst = []
        for i in range(len(res_dict)):
            reformat_dict = {}
            reformat_dict['cve_id'] = res_dict[i]['cve']['id']
            reformat_dict['descriptions'] = res_dict[i]['cve'][
                'descriptions'][0]['value']
            new_res_dict_lst.append(reformat_dict)

        return new_res_dict_lst

    def get_nvd_data_batch(self, url: str, api_key) -> typing.List[dict]:
        """
        Retrieves NVD data in batches using the provided URL and API key.

        Args:
            url (str): URL for NVD data retrieval.
            api_key: API key for authentication.

        Returns:
            list: List of NVD data dictionaries.
        """
        while True:
            try:
                print('[NVD url]', url)
                res = requests.get(url, api_key, headers=self.header)
                self.request_cd
                res_dict = json.loads(res.text)
                nvd_web_data_batch = self.reformat_nvd_dict_to_list(
                    res_dict['vulnerabilities'])
                break
            except Exception as e:
                print('[NVD url] Get cve error : ', e)

        return nvd_web_data_batch

    def get_all_nvd_web_data(self, url, api_key):
        """
        Retrieves all NVD web data, backs it up locally, and returns the data as a list.

        Args:
            url (str): Base URL for NVD data retrieval.
            api_key: API key for authentication.

        Returns:
            list: List of all NVD web data dictionaries.
        """
        nvd_web_data_all = []
        self.nvd = NvdCveDownloader(url, api_key)
        cvd_url_list = self.nvd.url_generator()
        for cvd_url in cvd_url_list:
            data_batch = self.nvd.get_nvd_data_batch(cvd_url, api_key)
            nvd_web_data_all.extend(data_batch)

        # back up cve to local data
        module_dir = os.path.dirname(__file__)
        dir_path = os.path.join(module_dir, 'nvdOutput')
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, 'nvdOutput.json')
        with open(file_path, 'w', newline='') as jsonfile:
            json.dump(nvd_web_data_all, jsonfile)

        return nvd_web_data_all

