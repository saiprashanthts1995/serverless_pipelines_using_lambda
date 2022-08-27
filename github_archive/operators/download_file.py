from github_archive.services.s3_service import S3Service

if __name__ == "__main__":
    s3 = S3Service()
    print(s3.s3_list_buckets())
    print(
        s3.s3_write_content("Hello ABC", "sai-ts-learn-tf", "landing_zone/Test/Hello.txt")
    )