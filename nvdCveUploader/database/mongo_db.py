import pymongo
from tqdm import tqdm
import datetime
from dotenv import load_dotenv
load_dotenv()


class KB():
    def __init__(self) -> None:
        self.dbClient = pymongo.MongoClient(
            'mongodb://<sever_ip>')

    def find_data(self, dbNm: str, colNm: str, query: dict = None):
        """Find Data from Database

        Args:
            dbNm: Database name.
            colNm: Collection name.
            Query: The query dict for finding data.
        Returns:
            List of data.
        """
        try:
            col = self.dbClient[dbNm][colNm]
            res = col.find(query)
            return list(res)
        except Exception as e:
            raise Exception(
                f'{e}, Failed to create data from {dbNm} database,',
                f' {colNm} collection.\nQuery:\n{query}')
        finally:
            self.dbClient.close()

    def insert_one_data(self, dbNm: str, colNm: str, data: dict):
        """Insert One Data into Database

        Args:
            dbNm: Database name.
            colNm: Collection name.
            data: The data which requires to insert.
        Returns:
            The data _id, database name, and collection name.
        """
        try:
            col = self.dbClient[dbNm][colNm]
            res = col.insert_one(data)
            print('Success: Insert {} into {} database, {} collection.'.format(
                res.inserted_id, dbNm, colNm))
        except Exception as e:
            print(e)
            raise Exception(
                f'Failed to create data in {dbNm} database,'
                f' {colNm} collection.')
        finally:
            self.dbClient.close()

    def insert_many_data(self, dbNm: str, colNm: str, data: dict, batch_size: int=100):
        """Insert many Data into Database base on batch size

        Args:
            dbNm: Database name.
            colNm: Collection name.
            data: The data which requires to insert.
        Returns:
            The data _id, database name, and collection name.
        """
        try:
            col = self.dbClient[dbNm][colNm]
            
            start = datetime.datetime.now()

            for i in tqdm(range(0, len(data), batch_size)):
                batch = data[i:i + batch_size] # cut data
                col.insert_many(batch)
            
            end = datetime.datetime.now()
            elapsed = end - start # Calculate insertion time
            print('Success: Insert {} data into {} database, {} collection.'.format(
                len(data), dbNm, colNm))
            print(f'Total elapsed time: {elapsed}')
        except Exception as e:
            print(e)
            raise Exception(
                f'Failed to create data in {dbNm} database,'
                f' {colNm} collection.')
        finally:
            self.dbClient.close()

    def update_one_data(self, dbNm: str, colNm: str, filter: dict, data: dict):
        """Update One Data in Database

        Args:
            dbNm: Database name.
            colNm: Collection name.
            filter: The filter query.
            data: The update data.
        Returns:
            The response of this action.
        """
        try:
            col = self.dbClient[dbNm][colNm]
            res = col.update_one(filter, data)
            print('Success: Update {} data in {} database, {} collection.'.format(
                res.modified_count, dbNm, colNm))
        except Exception as e:
            raise Exception(
                f'Failed to update data in {dbNm} database, {colNm} collection.')
        finally:
            self.dbClient.close()

    def delete_all_data(self, dbNm: str, colNm: str, filter: dict = {}):
        """Delete All Data in Database

        Args:
            dbNm: Database name.
            colNm: Collection name.
            filter: The filter query.
        Returns:
            The response of this action.
        """
        try:
            col = self.dbClient[dbNm][colNm]
            res = col.delete_many(filter)
            print('Success: Delete {} data in {} database, {} collection.'.format(
                res.deleted_count, dbNm, colNm))
        except Exception as e:
            raise Exception(
                f'{e},Failed to delete data in {dbNm} database, {colNm} collection.')
        finally:
            self.dbClient.close()

