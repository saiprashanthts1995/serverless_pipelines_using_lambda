import os

# sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from github_archive.services.s3_service import S3Service


def lambda_handler(event, context):
    s3 = S3Service()
    print(s3.s3_list_buckets())
    print(os.path.join(os.path.dirname(__file__)), "..")
    # call bookmark module to find the latest file
    # call create_file_path to get the list of files
    # call download file using the above list
    # update the bookmark table with the last extracted file


if __name__ == "__main__":
    s3 = S3Service()
    print(s3.s3_list_buckets())
    print(os.path.join(os.path.dirname(__file__)), "..")
