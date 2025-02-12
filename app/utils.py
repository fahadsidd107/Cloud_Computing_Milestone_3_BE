from google.cloud import storage
import logging

def upload_image_to_gcs(bucket, file, destination_blob_name):
    try:
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_file(file)
        image_url = f"https://storage.googleapis.com/{bucket.name}/{destination_blob_name}"
        logging.info(f"Image uploaded successfully: {image_url}")
        return image_url
    except Exception as e:
        logging.error(f"Failed to upload image: {str(e)}")
        raise
