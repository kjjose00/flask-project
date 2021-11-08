from flask import Flask,render_template,flash,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,date
from flask_migrate import Migrate
from wtforms.widgets import TextArea
from flskforms import Postform,userform,NamerForm,passwordform,LoginForm,SearchForm


from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,login_user,login_required,logout_user,current_user,LoginManager


app=Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Iamwork3*@localhost/our_users'
db=SQLAlchemy(app)
migrate=Migrate(app,db)

app.config['SECRET_KEY']='this is my secret key'

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))
class Posts(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(255))
    content=db.Column(db.Text)
    # author=db.Column(db.String(255))
    date_posted=db.Column(db.DateTime,default=datetime.utcnow)
    slug=db.Column(db.String(255))
    poster_id=db.Column(db.Integer,db.ForeignKey('users.id'))


# create a model
class users(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),nullable=False,unique=True)
    name=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(120),nullable=False,unique=True)
    favorite_color=db.Column(db.String(120))
    dateadded=db.Column(db.DateTime,default=datetime.utcnow)
    password_hash=db.Column(db.String(128))
    posts=db.relationship('Posts',backref='poster')
    @property
    def password(self):
	    raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
	    self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
	    return check_password_hash(self.password_hash, password)

   

	# Create A String
    def __repr__(self):
	    return '<Name %r>' % self.name

# pass stuff to navbar
@app.context_processor
def base():
    form=SearchForm()
    return dict(form=form)

@app.route('/search',methods=['POST'])
def search():
    form=SearchForm()
    posts=Posts.query
    if form.validate_on_submit():
        # print(post.searched)
        post.searched=form.searched.data
        posts=posts.filter(Posts.content.like("%"+post.searched+"%"))
        posts=posts.order_by(Posts.title).all()
        return render_template('search.html',form=form,searched=post.searched,posts=posts)

  
@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=users.query.filter_by(username=form.username.data).first()
        if user:
            #check the hash
            if check_password_hash(user.password_hash,form.password.data):
                login_user(user)
                flash('login successful!!!')
                return redirect(url_for('dashboard'))
            else:
                flash('wrong password!Try again')
        else:
            flash('That user does not exists')


    return render_template('login.html',form=form)

@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("you have successfully logged out!!!")
    return redirect(url_for('login'))

@app.route('/posts/<int:id>')
def post(id):
    post=Posts.query.get_or_404(id)
    return render_template('post.html',post=post)
@app.route('/posts',methods=['GET'])
def posts():
    posts=Posts.query.order_by(Posts.date_posted)
    return render_template('posts.html',posts=posts)
@app.route('/addpost',methods=['GET','POST'])
@login_required
def add_post():
    form=Postform()
    if form.validate_on_submit():
        poster=current_user.id
        post=Posts(title=form.title.data,content=form.content.data,poster_id=poster,slug=form.slug.data)
        form.title.data=''
        form.content.data=''
        
        form.slug.data=''
        db.session.add(post)
        db.session.commit()
        flash('blog post added successfully!!!')
    return render_template("add_post.html",form=form)

@app.route('/edit_post/<int:id>',methods=['GET','POST'])
def edit_post(id):
    post=Posts.query.get_or_404(id)
    form=Postform()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
       
        post.slug=form.slug.data
        form.title.data=''
        form.content.data=''
        
        form.slug.data=''
        db.session.add(post)
        db.session.commit()
        flash("successfully updated post")
    if current_user.id==post.poster_id:
        form.title.data=post.title
        form.content.data=post.content
        
        form.slug.data=post.slug
        return render_template("edit_post.html",form=form,post=post)
    else:
        flash('youare not authorized to do edit this post...')
        posts=Posts.query.order_by(Posts.date_posted)
        return render_template('posts.html',posts=posts)

@app.route('/delete_post/<int:id>',methods=['GET','POST'])
@login_required
def delete_post(id):
    post_to_delete=Posts.query.get_or_404(id)
    id=current_user.id
    if id==post_to_delete.poster.id:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            flash("successfully deleted post")
            posts=Posts.query.order_by(Posts.date_posted)
            return render_template("posts.html",posts=posts)

        except:
            flash("something went wrong try again!!!")
            posts=Posts.query.order_by(Posts.date_posted)
            return render_template("posts.html",posts=posts)
    else:
        flash("you are not authorised to delete!!!")
        posts=Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html",posts=posts)




# dhfgdfdg
@app.route('/date',methods=['GET'])
def get_date():
    books={
    'bible':'jesus',
    'rosary':'mary',
    'holy mass':"church"
    }
    return books
@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete=users.query.get_or_404(id)
    name=None
    form=userform()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('user deleted successfully!!!')
        our_users = users.query.order_by(users.dateadded)
        return render_template('add_user.html',form=form,name=name,our_users=our_users)
    except:
        flash("some problem in deleting ...try again!!")
        our_users = users.query.order_by(users.dateadded)
        return render_template('add_user.html',form=form,name=name,our_users=our_users)

@app.route('/update/<int:id>',methods=['GET','POST'])
@login_required
def update(id):
    form=userform()
    name_to_update=users.query.get_or_404(id)
    if request.method=='POST':
        name_to_update.name=request.form['name']
        name_to_update.email=request.form['email']
        name_to_update.favorite_color=request.form['favorite_color']
        name_to_update.username=request.form['username']
        try:
            db.session.commit()
            flash('updated successfully')
            name=form.name.data
            form.name.data=''
            form.email.data=''
            form.username.data=''
            form.favorite_color.data=''
            
            our_users=users.query.order_by(users.dateadded)
            return render_template('update.html',form=form,name_to_update=name_to_update,name=name,our_users=our_users,id=id)
        except:
            flash('error.......try again!!')
            return render_template('update.html',form=form,name_to_update=name_to_update,id=id)
    else:
        return render_template('update.html',form=form,name_to_update=name_to_update,id=id)

        




@app.route('/users/add',methods=['GET','POST'])
def add_user():
    name=None
    form=userform()
    
    if form.validate_on_submit():
        user=users.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_pw = generate_password_hash(form.password_hash.data,"sha256")
           
            user=users(name=form.name.data,username=form.username.data,email=form.email.data,favorite_color=form.favorite_color.data,password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        
        name=form.name.data
        form.name.data=''
        form.username.data=''
        form.email.data=''
        form.favorite_color.data=''
        form.password_hash.data =''
       
        flash('user added successfully')
    our_users=users.query.order_by(users.dateadded)
    return render_template('add_user.html',form=form,our_users=our_users,name=name)

@app.route('/')
def hello():
    name="God"
    stuff=['one','two','three','four','five',45]
    return render_template('index.html',uname=name,stuff=stuff)

@app.route('/user/<name>')
def user(name):
    return render_template('hello.html',user_name=name)

@app.errorhandler(404)
def pagenotfound(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def pagenotfound(e):
    return render_template('500.html'),500

@app.route('/check_pw',methods=['GET','POST'])
def check_password():
   
    email=None
    passed=None
    password=None
    pw_to_find=None
    form=passwordform()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        form.email.data=''
        form.password.data=''
        pw_to_find=users.query.filter_by(email=email).first()
        
        passed=check_password_hash(pw_to_find.password_hash,password)
    return render_template('password_check.html',email=email,password=password,form=form,pw_to_find=pw_to_find,passed=passed)
       
  
        



        
   

    

@app.route('/name',methods=['GET','POST'])
def name():
    name=None
    form=NamerForm()
    if form.validate_on_submit():
        name=form.name.data
        form.name.data=''
        flash('form submitted successfully')
    return render_template('name.html',name=name,form=form)


if __name__=="__main__":
    app.run(debug=True)
