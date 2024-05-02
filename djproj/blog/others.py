def upload_to_author_directory(instance, filename):
    author_name = instance.post.author.username  # assuming Post model has an author field
    return f"{author_name}/{filename}"