from flask_restful import Resource, reqparse

from flask_jwt_extended import jwt_required,get_jwt_identity

from models.store import StoreModel                            


class Store(Resource):

    parser = reqparse.RequestParser()                      

    parser.add_argument('name',                       
        type = str,
        required = True,
        help = "Store name field cannot be left blank!"
    )


    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.json()
        return {'message': 'Store not found'}, 404


    @jwt_required()
    def post(self, name):
        data = Store.parser.parse_args()

        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400

        store = StoreModel(**data)                                # creates a new store instance
        # Alternative code ==> store = StoreModel(name)      
                                  
        try:
            store.save_to_db()                                 
        except:
            return {"message": "An error occurred creating the store."}, 500

        return store.json(), 201                                

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}


class StoreList(Resource):
    @jwt_required()
    def get(self):
        return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}              
        # Alternative Code ==>  return {'items': [x.json for x in StoreModel.query.all()]}      


    


