import sys
from datetime import datetime
import time


class GithubArchiveConf:
    BOOKMARK_TABLE_NAME = "bookmark-github"
    BOOKMARK_TABLE_ID = 1
    STORAGE_FILE_PATH = "github_archive/download/"
    BUCKET_NAME = "sai-ts-learn-tf"
    BOOKMARK_ATTRIBUTES = {
        "TABLE_ID": ["S", "HASH"],
        "TABLE_NAME": ["S", "RANGE"],
        "FILE_LOAD_TIMESTAMP": ["N", "ATTRIBUTE"],
        "LAST_EXTRACTED_FILE": ["S", "ATTRIBUTE"],
    }
    URL_PREFIX = "https://data.gharchive.org/"
    INITIAL_FILE_NAME = "2022-09-04-15.json.gz"

    @staticmethod
    def get_key_schema() -> list:
        key_schema = list()
        for key, value in GithubArchiveConf.BOOKMARK_ATTRIBUTES.items():
            if value[1] in ["HASH", "RANGE"]:
                schema = {"AttributeName": key, "KeyType": value[1]}
                key_schema.append(schema)
        return key_schema

    @staticmethod
    def get_key_attributes() -> list:
        key_attributes = list()
        for key, value in GithubArchiveConf.BOOKMARK_ATTRIBUTES.items():
            if value[1] in ["HASH", "RANGE"]:
                attribute = {"AttributeName": key, "AttributeType": value[0]}
                key_attributes.append(attribute)
        return key_attributes

    @staticmethod
    def get_filter_expression() -> dict:
        filter_expressions = dict()
        for key, value in GithubArchiveConf.BOOKMARK_ATTRIBUTES.items():
            if key == "TABLE_ID":
                filter_expressions[key] = {
                    value[0]: str(GithubArchiveConf.BOOKMARK_TABLE_ID)
                }
            elif key == "TABLE_NAME":
                filter_expressions[key] = {
                    value[0]: GithubArchiveConf.BOOKMARK_TABLE_NAME
                }
            else:
                pass
        return filter_expressions

    @staticmethod
    def entry_item(file_type="first", file_name="") -> dict:
        entry_item = dict()
        for key, value in GithubArchiveConf.BOOKMARK_ATTRIBUTES.items():
            if key == "TABLE_ID":
                entry_item[key] = {value[0]: str(GithubArchiveConf.BOOKMARK_TABLE_ID)}
            elif key == "TABLE_NAME":
                entry_item[key] = {value[0]: GithubArchiveConf.BOOKMARK_TABLE_NAME}
            elif key == "FILE_LOAD_TIMESTAMP":
                entry_item[key] = {value[0]: str(GithubArchiveConf.get_epoch_time())}
            elif key == "LAST_EXTRACTED_FILE":
                if file_type == "first":
                    entry_item[key] = {
                        value[0]: GithubArchiveConf.URL_PREFIX
                        + GithubArchiveConf.INITIAL_FILE_NAME
                    }
                else:
                    entry_item[key] = {value[0]: file_name}

            else:
                print("Add new entries to BOOKMARK_ATTRIBUTES dictionary ")
                sys.exit(1)
        return entry_item

    @staticmethod
    def get_epoch_time():
        pattern = "%Y-%m-%d %H:%M:%S"
        ts = datetime.strftime(datetime.now(), pattern)
        return int(time.mktime(time.strptime(ts, pattern)))


if __name__ == "__main__":
    conf = GithubArchiveConf()
    print(conf.get_key_schema())
    print(conf.get_key_attributes())
    print(conf.get_filter_expression())
    print(conf.get_epoch_time())
    print(conf.entry_item())
