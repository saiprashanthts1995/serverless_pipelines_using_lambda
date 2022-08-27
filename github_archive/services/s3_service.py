import boto3
import os


class S3Service:
    def __init__(self) -> None:
        os.environ.setdefault('AWS_PROFILE', 'serverless')
        self.s3_client = boto3.client('s3')

    def s3_list_buckets(self):
        print(self.s3_client.list_buckets())
        print(os.getenv('BUCKET_NAME'))

    def s3_write_content(self, content):
        pass


if __name__ == '__main__':
    s3 = S3Service()
    s3.s3_list_buckets()
