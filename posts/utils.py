# this function genarate dynamic path to store users profile images
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'posts/media/image_id_{instance.id}/{filename}'