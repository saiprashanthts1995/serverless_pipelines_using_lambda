import time
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
        time.sleep(20)
        db.write_to_table(
            table_name=GithubArchiveConf.BOOKMARK_TABLE_NAME,
            item=GithubArchiveConf.entry_item(),
        )
        print("Initial entry to the table is made successfully")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            print("Table in DynamoDB already exists.")
            print("Continuing with the process")
        else:
            print(e)
            sys.exit(1)


def retrieve_last_file_name():
    db = DynamoService()
    output_response = db.retrieve_table_content_using_get(
        table_name=GithubArchiveConf.BOOKMARK_TABLE_NAME,
        filter_expression=GithubArchiveConf.get_filter_expression(),
    )
    print(output_response["LAST_EXTRACTED_FILE"]["S"])


def update_table_content(file_name):
    db = DynamoService()
    db.write_to_table(
        table_name=GithubArchiveConf.BOOKMARK_TABLE_NAME,
        item=GithubArchiveConf.entry_item(file_type="Updated", file_name=file_name),
    )
    print(f"Dynamodb table updated with the filename {file_name} ")


if __name__ == "__main__":
    create_bookmark_table()
    retrieve_last_file_name()
    # update_table_content("Sai")
