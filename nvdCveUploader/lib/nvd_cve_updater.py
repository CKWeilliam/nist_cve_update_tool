import os
import re
import glob
import json
from deepdiff import DeepDiff
from ast import literal_eval
from database.mongo_db import KB
from dotenv import load_dotenv
load_dotenv()


class CveUpdater():
    def __init__(self) -> None:
        self.db_collection = 'kb'
        self.col = 'nvd_lst'
        self.url = 'mongodb://<sever_ip>/'
        self.kb_db = KB(
            os.getenv('DEV_DB_IP'),
            os.getenv('DEV_DB_PORT'),
            'kb'
            )

    def get_db_data(self, db, col):
        db_data = self.kb_db.find_data(col)

        return db_data

    def update_cve(self, update_index, db_data, online_data):
        for item_mapping in update_index:

            item_index = item_mapping[0]
            self.kb_db.update_one_data(
                self.col, db_data[item_index],
                {"$set": online_data[item_index]}
                )

    def insert_cve(self, add_index, online_data):
        for item_mapping in add_index:

            item_index = item_mapping[0]
            self.kb_db.insert_one_data(
                self.col, online_data[item_index]
                )

    def str_diff_parse(self, str_diff):
        return [tuple(
                literal_eval(y) for y in re.findall(
                    r"\[('?\w+'?)\]", x)) for x in str_diff]

    def compare_and_update(self, db_data: list, online_data: list) -> list:
        """Compare and update DB data from online data.

            Args:
                db_data: List of dict from DB (old data).
                online_data: List of dict from online (new data).
            Returns:
                List of dict. (updated DB data)
        """

        diff = DeepDiff(db_data, online_data)

        update_index = []
        add_index = []

        if "values_changed" in diff:
            updated = diff["values_changed"]
            update_index = self.str_diff_parse(updated)

        if "iterable_item_added" in diff:
            added = diff["iterable_item_added"]
            add_index = self.str_diff_parse(added)

        return update_index, add_index

    def nvd_cve_update_and_insert(self, cve_web_data):
        db_data = self.get_db_data(self.db, self.col)
        online_data = cve_web_data

        update_index, add_index = self.compare_and_update(
            db_data, online_data)

        self.update_cve(update_index, db_data, online_data)
        self.insert_cve(add_index, online_data)
        print(f'Update item : {len(update_index)} pieces')
        print(f'Add item : {len(add_index)} pieces')

    # Read local cve json data
    def web_data_json(self):
        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, 'nvdOutput', '*.json')
        web_data = []
        json_paths = glob.glob(file_path)
        for json_path in json_paths:
            with open(json_path, 'r') as jsonfile:
                data = json.load(jsonfile)
                web_data.extend(data)
        print('localData : ', len(web_data), 'pieces')

        return web_data
