from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)
app.config['DEBUG'] = True
# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode2@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/')
def index():

    return redirect("/blog")

@app.route('/blog')
def blog_list():
    #Retrieve query arguments for the url if the user was redirected here.
    blog_id = request.args.get("id")

    if(blog_id):
        blog_id = int(blog_id)
        blogs = Blog.query.filter_by(id=blog_id).all()
        return render_template('blog-entry.html',title="Blog Entry", blogs=blogs)
    else:
        #show blog entries in asending order 
        #blogs = Blog.query.all()

        #show blog entries in desending order 
        blogs = Blog.query.order_by((desc(Blog.id))).all()

        return render_template('blog-listing.html',title="Blog List", blogs=blogs)

@app.route('/new-post')
def new_post():
    #Retrieve query arguments for the url if the user was redirected here.
    btitle = request.args.get("btitle")
    text = request.args.get("bbody")
    terror = request.args.get("terror")
    berror = request.args.get("berror")

     #If the title and body aren't sent as query parameters the previous statements set to None.
    #In that case, they need to be set to empty strings.
    if btitle == None:
        btitle = ""
    if text == None:
        text = ""

    #display the signup form.
    return render_template("new-post.html", title="Add a new Blog entry", blog_title=btitle, blog_post=text, terror=terror, berror=berror)

@app.route('/add-entry', methods=['POST'])
def add_entry():

    blog_name = request.form['blog_title']
    blog_text = request.form['blog_text']

    #initialize error messages
    title_error = ""
    body_error = ""
    error_query = ""
    
    if (blog_name == ""):
        # the user tried to enter an invald blog title
        # so we redirect back to the front page and tell them what went wrong
        title_error = "Please enter title for your blog entry."
    
    if (blog_text == ""):
        # the user tried to enter a blank post body,
        # so we redirect back to the front page and tell them what went wrong
        body_error = "Please enter the body of your blog entry."

    if (title_error != ""):
            error_query += "&terror=" + title_error

    if (body_error != ""):
            error_query += "&berror=" + body_error

    if (error_query != ""):
        # redirect to homepage, and include error as a query parameter in the URL.
        return redirect("/new-post?btitle=" + blog_name + "&bbody=" + blog_text + error_query)
    else:    
        # if we didn't redirect by now, then all is well
        new_blog = Blog(blog_name, blog_text)
        db.session.add(new_blog)
        db.session.commit()
        
        #Use Case 1
        #return redirect("/blog")

        #Use Case 2 
        blogs = Blog.query.filter_by(id=new_blog.id).all()
        return render_template('blog-entry.html',title="Blog Entry", blogs=blogs)

if __name__ == "__main__":
    app.run()