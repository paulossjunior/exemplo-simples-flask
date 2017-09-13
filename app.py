import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)

app.config['SECRET_KEY'] = '123456790'

# Criando um banco em memoria
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sample_db_2.sqlite'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# Flask views
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
    
# Flask views
@app.route('/add',methods=['POST'])
def save_user():
    try:
        #Pegando dados do formulario
        nome = request.form['nome']
        senha = request.form['password']
        email = request.form['email']
        rua = request.form['rua']
	
        address = Address(rua)
        user = User(nome,email,senha)
        user.address = address
    	
    	#Salvando o usuario
        db.session.add(user)
        db.session.commit()  
        
        db.session.add(address)
        db.session.commit()  
        
        usuarios = User.query.all()
        return render_template("usuarios.html", usuarios=usuarios)
    
    except SQLAlchemyError:
        
        return render_template('index.html')    
        
class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

class User(Base):

    __tablename__ = 'user'

    # User Name
    name    = db.Column(db.String(128),  nullable=False)

    # Identification Data: email & password
    email    = db.Column(db.String(128),  nullable=False,
                                            unique=True)
    password = db.Column(db.String(192),  nullable=False)
    
    addresses = db.relationship("Address")

    # New instance instantiation procedure
    def __init__(self, name, email, password):

        self.name     = name
        self.email    = email
        self.password = password

    def __repr__(self):
        mensagem = self.name +'-'+self.email+'-'+self.password              
        
        for address in self.addresses:
            mensagem += address.street
        
        return mensagem

class Address(Base):
    
    __tablename__= 'address'   
    
    street = db.Column(db.String(255),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # New instance instantiation procedure
    def __init__(self, street):

        self.street     = street
        

    def __repr__(self):
        return '<Address %r>' % (self.street)              


if __name__ == '__main__':

    #Criando o banco
    db.create_all()
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))