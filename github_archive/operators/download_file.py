import sys

import requests

from github_archive.services.s3_service import S3Service


def download_file(path: str) -> bytes:
    """
    This udf is used for downloading the files from the
     gitHub archive website and returns the file content
     in bytes
    Args:
        path: path to be downloaded

    Returns: the file content in byte
    """
    response = requests.get(path)
    if response.status_code == 200:
        print(f"File {path} got downloaded successfully")
        return response.content
    else:
        print("Process of downloading the file got failed.")
        sys.exit(1)


if __name__ == "__main__":
    s3 = S3Service()
    download_file("https://data.gharchive.org/2015-01-01-15.json.gz")
