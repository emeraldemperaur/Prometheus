from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, jwt_optional, get_jwt_identity
from models.item import ItemModel



class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left null!"

    )
    parser.add_argument('store_id',
        type=float,
        required=True,
        help="Every item needs a store id!"

    )

    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': "Item '{}' not found".format(name)}, 404



    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "Item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "Error occured inserting the item"}, 500

        return item.json(), 201

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Sorry, Emperaur priviledge required to delete data'}

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': "Item '{}' deleted".format(name)}



    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)


        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()



class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {'items': items}, 200
        return {
            'items': [items[0]['name'] for item in items],
            'message': 'More data availble to authorized users'
        }, 200
        
