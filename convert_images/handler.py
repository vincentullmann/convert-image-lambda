"""Entry Point for the Lambda."""

# IMPORT STANDARD LIBRARIES
import io
import os

# IMPORT THIRD PARTY LIBRARIES
from botocore.exceptions import ClientError
from PIL import Image
import boto3


s3 = boto3.client("s3")


EXTENSIONS = (".png", ".jpg", ".jpeg")


def convert(bucket: str, path: str):

    # Load
    try:
        source_image = s3.get_object(Bucket=bucket, Key=path)
    except ClientError as e:
        print(e)
        return

    image = Image.open(source_image["Body"])

    # Save to Buffer
    buffer = io.BytesIO()
    image.save(buffer, format="webp")

    basename, _ = os.path.splitext(path)
    new_path = f"{basename}.webp"

    # Save Buffer to S3
    sent_data = s3.put_object(
        Bucket=bucket,
        Key=new_path,
        Body=buffer.getvalue(),
        ContentType="image/webp",
        CacheControl=source_image.get("CacheControl"),
    )
    print(sent_data)
    # if sent_data['ResponseMetadata']['HTTPStatusCode'] != 200:
    #     raise S3ImagesUploadFailed('Failed to upload image {} to bucket {}'.format(key, bucket))


def main(event, context=None):

    for record in event.get("Records") or []:
        info = record.get("s3", {})
        bucket = info.get("bucket", {}).get("name", "")
        path = info.get("object", {}).get("key", "")

        if not (bucket and path):
            continue

        if not path.endswith(EXTENSIONS):
            continue

        convert(bucket=bucket, path=path)

    return {
        'statusCode': 200,
    }
