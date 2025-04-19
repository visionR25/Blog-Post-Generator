from utils import save_blog, list_saved_blogs, load_blog, delete_blog, export_to_pdf, export_to_markdown

# Test save_blog
filename = save_blog("Hats", "Hats are the best.", {"tone": "Casual", "length": "Short"})
print(f"Saved blog as: {filename}")

# Test list_saved_blogs
blogs = list_saved_blogs()
print(f"Saved blogs: {blogs}")

# Test load_blog
# if blogs:
#     blog_data = load_blog(blogs[0])
#     print(f"Loaded blog: {blog_data}")

# Test delete_blog
# if blogs:
#     delete_blog(blogs[0])
#     print(f"Deleted blog: {blogs[0]}")