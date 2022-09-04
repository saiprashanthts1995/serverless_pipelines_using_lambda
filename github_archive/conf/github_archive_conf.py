class GithubArchiveConf:
    BOOKMARK_TABLE_NAME = "bookmark-github"
    BOOKMARK_TABLE_ID = 1
    STORAGE_FILE_PATH = "github_archive/download/"
    BUCKET_NAME = ""
    BOOKMARK_ATTRIBUTES = {
        "TABLE_ID": ["S", "HASH"],
        "TABLE_NAME": ["S", "RANGE"],
        "FILE_LOAD_TIMESTAMP": ["N", "ATTRIBUTE"],
        "LAST_EXTRACTED_FILE": ["S", "ATTRIBUTE"],
    }

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
                    value[0]: GithubArchiveConf.BOOKMARK_TABLE_ID
                }
            elif key == "TABLE_NAME":
                filter_expressions[key] = {
                    value[0]: GithubArchiveConf.BOOKMARK_TABLE_NAME
                }
            else:
                pass
        return filter_expressions


if __name__ == "__main__":
    conf = GithubArchiveConf()
    print(conf.get_key_schema())
    print(conf.get_key_attributes())
    print(conf.get_filter_expression())
