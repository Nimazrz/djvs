def upload_to_author_directory(request, filename):
    author_name = request.post.author.username  # assuming Post model has an author field
    return f"{author_name}/{filename}"
