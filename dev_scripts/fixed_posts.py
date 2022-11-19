import os

class Fixed_Posts:

    booklist = """
    ---
    title: "Book List"
    date: "2022-04-01"
    description: "More Resources To Reference"
    tags: [
    ]
    categories: [
    ]
    type: "post"
    ---
    ### Preview
    - You cannot read all books containing valuable information in a thousand lifetimes. 
    - The trick is knowing which ones to read.
    - This list has the possibility of being modified over time.

    ### [Free Books](https://books.dev00ps.com)
    """

    fixed_posts = {
        "Booklist.md": booklist
    }


    def write_post(self, post_dir, post_name, content):
        with open(post_dir + post_name, "w") as f:
            f.write(content)
            print("Post generated: " + post_dir + post_name)
        f.close()

        

    def __init__(self, posts_dir):

        if not os.path.exists(posts_dir):
            os.mkdir(posts_dir)
        for filename in self.fixed_posts:
            if not os.path.exists(posts_dir + filename):
                self.write_post(posts_dir, filename, self.fixed_posts[filename])