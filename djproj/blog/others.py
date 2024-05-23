def upload_to_author_directory(request, filename):
    author_name = request.post.author.username  # assuming Post model has an author field
    return f"post-images/{author_name}/{filename}"

def upload_to_author_directory_account(instance, filename):
    author_name = instance.user.username  # assuming instance has an author field
    return f'account-images/{author_name}/{filename}'