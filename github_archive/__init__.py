import os

from github_archive.conf.github_archive_conf import GithubArchiveConf
from github_archive.operators.bookmark import (create_bookmark_table,
                                               update_table_content)
from github_archive.operators.create_file_path import generate_file_name
from github_archive.operators.download_file import download_file
# sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from github_archive.services.s3_service import S3Service
from github_archive.utlis import udf_exception


@udf_exception
def main():
    s3 = S3Service()
    conf = GithubArchiveConf()
    # create the table if not exists
    create_bookmark_table()
    # call generate_file_name to get the list of files
    file_list = generate_file_name()
    print(
        f"Files will be downloaded to the bucket {conf.BUCKET_NAME} under the prefix {conf.STORAGE_FILE_PATH}"
    )
    if len(file_list) > 0:
        for file in file_list:
            # call download file using the above list
            file_content = download_file(file)
            s3.s3_write_content(
                content=file_content,
                bucket_name=conf.BUCKET_NAME,
                file_name=conf.STORAGE_FILE_PATH + file.split("/")[-1],
            )
        # update the bookmark table with the last extracted file
        update_table_content(file_name=file_list[-1])
    else:
        print("No files to download. Bookmark table is having the latest tabl entry")
        print("All files are already downloaded")


def lambda_handler(event, context):
    print("Process Started")
    main()
    print("Process completed")


if __name__ == "__main__":
    s3 = S3Service()
    print("List of buckets present")
    print(s3.s3_list_buckets())
    print(os.path.join(os.path.dirname(__file__)), "..")
    lambda_handler(None, None)
