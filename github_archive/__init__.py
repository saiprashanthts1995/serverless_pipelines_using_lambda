import sys
import os
# sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from github_archive.services.s3_service import S3Service

def lambda_handler(event, context):
    s3 = S3Service()
    print(s3.s3_list_buckets())
    print(os.path.join(os.path.dirname(__file__)),"..")


if __name__ == "__main__":
    s3 = S3Service()
    print(s3.s3_list_buckets())
    print(os.path.join(os.path.dirname(__file__)),"..")

