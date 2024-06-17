import os


def receipt_image_upload_path(instance, filename):
    # Construct the image upload path based on user id and date
    upload_folder = f"user_{instance.user.id}/{instance.dated.strftime('%Y%m%d')}"
    return os.path.join("receipt_images", upload_folder, filename)
