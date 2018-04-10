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
    
    #Define fields in the Blog table 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    
    #Constructor for the Blog class
    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/')
def index():

    return redirect("/blog")

#route for displaying a list of blog entries
@app.route('/blog')
def blog_list():
    #Retrieve query arguments for the url if the user was redirected here.
    blog_id = request.args.get("id")

    # if the url contain query arguments, display the log entry associated with the id 
    # in the query argument
    if(blog_id):
        blog_id = int(blog_id)
        blogs = Blog.query.filter_by(id=blog_id).all()
        return render_template('blog-entry.html', title="Blog Entry", blogs=blogs)
    else:
        #show all blog entries in asending order 
        #blogs = Blog.query.all()

        #show all blog entries in desending order 
        blogs = Blog.query.order_by((desc(Blog.id))).all()

        return render_template('blog-listing.html', title="Blog List", blogs=blogs)

#route for displaying the form to add a new blog entry.
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

    #display the new-post form.
    return render_template("new-post.html", title="Add a new Blog entry", blog_title=btitle, blog_post=text, terror=terror, berror=berror)

#route for processing the form to add a new blog entry.
@app.route('/add-entry', methods=['POST'])
def add_entry():

    #get info from the form.
    blog_name = request.form['blog_title']
    blog_text = request.form['blog_text']

    #initialize error messages
    title_error = ""
    body_error = ""
    error_query = ""
    
    if (blog_name == ""):
        # the user tried to enter a blank blog title
        # so we redirect back to the form page and tell them what went wrong
        title_error = "Please enter title for your blog entry."
    
    if (blog_text == ""):
        # the user tried to enter a blank post body,
        # so we redirect back to the form page and tell them what went wrong
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

        #Add new blog entry to the database
        new_blog = Blog(blog_name, blog_text)
        db.session.add(new_blog)
        db.session.commit()
        
        #Use Case 1
        #return to the list of all blog entries
        #return redirect("/blog")

        #Use Case 2
        #Show the new blog entry
        blogs = Blog.query.filter_by(id=new_blog.id).all()
        return render_template('blog-entry.html',title="Blog Entry", blogs=blogs)

if __name__ == "__main__":
    app.run()