import os


def receipt_image_upload_path(instance, filename):
    # Construct the image upload path based on user id and date
    # Example: receipt_images/user_1/20210101/receipt.jpg
    upload_folder = f"user_{instance.id}/{instance.dated.strftime('%Y%m%d')}"
    return os.path.join("receipt_images", upload_folder, filename)
