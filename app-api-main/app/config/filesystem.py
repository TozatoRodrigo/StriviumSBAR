from app.core.environment import envs

driver = envs.FILESYSTEM_DRIVER

configs = {
    "local": {
        "base_url": envs.APP_URL,
    },
    "gcs": {
        "base_url": envs.GCS_BASE_URL,
        "project_id": envs.GCS_PROJECT_ID,
        "bucket_name": envs.GCS_BUCKET_NAME,
        "key_file": envs.GCS_KEY_FILE,
    },
    "s3": {
        "public_url": envs.S3_PUBLIC_URL,
        "bucket_name": envs.S3_BUCKET_NAME,
        "endpoint_url": envs.S3_ENDPOINT_URL,
        "aws_access_key_id": envs.S3_AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": envs.S3_AWS_SECRET_ACCESS_KEY,
    },
    "fake": {},
}
