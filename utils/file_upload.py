import os
import shutil


def avatar_path(instance, filename):
    profile = instance.user.username
    return 'profiles/{}/{}'.format(profile, filename)


def media_delete_path(media):
    path = os.path.abspath(os.path.join(media.path, '..'))
    shutil.rmtree(path)


def post_media_path(instance, filename):
    post = instance.post.id
    return 'posts/{}/{}'.format(post, filename)
