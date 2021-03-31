from flask import Blueprint,Flask,request,render_template
from flask_paginate import Pagination, get_page_parameter
from flask_sqlalchemy import SQLAlchemy

mod = Blueprint('users', __name__)

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(),nullable=False)
    email=db.Column(db.String(),nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

@mod.route('/')
def index():
    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = request.args.get(get_page_parameter(), type=int, default=1)

    user_count = User.query.count()
    users=User.query.all()
    pagination = Pagination(page=page, total=user_count, search=search, record_name='users',per_page=3)
    # 'page' is the default name of the page parameter, it can be customized
    # e.g. Pagination(page_parameter='p', ...)
    # or set PAGE_PARAMETER in config file
    # also likes page_parameter, you can customize for per_page_parameter
    # you can set PER_PAGE_PARAMETER in config file
    # e.g. Pagination(per_page_parameter='pp')

    return render_template('index.html',
                           users=users,
                           pagination=pagination,
                           )



app.register_blueprint(mod)

@app.shell_context_processor
def make_shell_context():
    return {
        'app':app,
        'db':db,
        'User':User
    }

if __name__ == '__main__':
    app.run(debug=True)
