from flask import Flask
from flask_restful import Api

from flask_jwt_extended import JWTManager

from resources.user import UserRegister, UserLogin, User, TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)                                               

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/store_database'    # for MySQL database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store_database.db'             # for sqlite database 

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False                
app.config['PROPAGATE_EXCEPTIONS'] = True                           
app.secret_key = '190bbfad3958fad815af8029ce0ce7e2cf966bd0c919b2586ce7ed7e785edc82' 
api = Api(app)                                                      


app.config['JWT_SECRET_KEY'] = '190bbfad3958fad815af8029ce0ce7e2cf966bd0c919b2586ce7ed7e785edc82'  
app.config['JWT_BLACKLIST_ENABLED'] = True                              
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']        
jwt = JWTManager(app)                                                  


@app.before_first_request                                           
def create_tables():                                                
    db.create_all()                                                 


api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')

# api.add_resource(User, '/user/<int:user_id>')

if __name__ == '__main__':                                          
    from db import db                                               
    db.init_app(app)                                                
    app.run(port=5000, debug = True)                                
