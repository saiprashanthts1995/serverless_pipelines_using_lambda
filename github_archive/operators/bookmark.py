from github_archive.conf.github_archive_conf import GithubArchiveConf
from github_archive.services.dynamo_services import DynamoService
from botocore.errorfactory import ClientError
import sys


def create_bookmark_table():
    db = DynamoService()
    try:
        db.create_table(
            table_name=GithubArchiveConf.BOOKMARK_TABLE_NAME,
            key_schema=GithubArchiveConf.get_key_schema(),
            attributes_definition=GithubArchiveConf.get_key_attributes(),
        )
        print(
            f"Table {GithubArchiveConf.BOOKMARK_TABLE_NAME} in DynamoDB "
            f"got created successfully"
        )
        db.write_to_table()
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            print("Table in DynamoDB already exists.")
            print("Continuing with the process")
        else:
            print(e)
            sys.exit(1)


if __name__ == "__main__":
    create_bookmark_table()
