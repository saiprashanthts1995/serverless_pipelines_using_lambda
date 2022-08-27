import boto3
import os
from github_archive.utlis import udf_exception


class S3Service:
    def __init__(self) -> None:
        os.environ.setdefault("AWS_PROFILE", "serverless")
        self.s3_client = boto3.client("s3")

    def s3_list_buckets(self) -> list:
        """
        This Udf is used to list the buckets available in the account
        Returns: list of buckets
        """
        list_buckets_response = self.s3_client.list_buckets()
        print(list_buckets_response)
        bucket_list = [bucket["Name"] for bucket in list_buckets_response["Buckets"]]
        return bucket_list

    @udf_exception
    def s3_write_content(self, content, bucket_name, file_name):
        put_response = self.s3_client.put_object(
            Body=content.encode("utf-8"),
            Bucket=bucket_name,
            Key=file_name,
        )
        return put_response


if __name__ == "__main__":
    s3 = S3Service()
    print(s3.s3_list_buckets())
    print(
        s3.s3_write_content("Hello", "sai-ts-learn-tf", "landing_zone/Test/Hello.txt")
    )
