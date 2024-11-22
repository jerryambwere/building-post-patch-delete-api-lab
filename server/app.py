#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(  bakeries,   200  )

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):

    bakery = Bakery.query.filter_by(id=id).first()
    bakery_serialized = bakery.to_dict()
    return make_response ( bakery_serialized, 200  )

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    return make_response( baked_goods_by_price_serialized, 200  )
   

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return make_response( most_expensive_serialized,   200  )

# @app.route('/baked_goods')
# def create_baked_goods():
#     name=request.form.get('name')
#     price=request.form.get('price')

#     new_baked_good=BakedGood(name=name,price=price)
#     db.session.add(new_baked_good)
#     db.session.commit()
#     return jsonify({
#         'id':new_baked_good.id,
#         'name':new_baked_good.name,
#         'price':new_baked_good.price
#     }),201

# @app.route('/bakeries/<int:id>')
# def update_bakery(id):
#     bakery=Bakery.query.get_or_404(id)
#     new_name=request.form.get('name')
#     if new_name:
#         bakery.name=new_name

#     db.session.commit()
#     # Return the updated bakery as JSON
#     return jsonify({
#         'id': bakery.id,
#         'name': bakery.name
#     }), 200  # 200: OK

# @app.route('/baked_goods/<int:id>', methods=['DELETE'])
# def delete_baked_good(id):
#     # Find the baked good by ID
#     baked_good = BakedGood.query.get_or_404(id)

#     # Delete the record
#     db.session.delete(baked_good)
#     db.session.commit()

#     # Return confirmation as JSON
#     return jsonify({'message': f'Baked good with id {id} was successfully deleted.'}), 200

#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from sqlalchemy import desc
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    response = make_response(bakeries, 200)
    return response

@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    
    if not bakery:
        return make_response({"error": "Bakery not found"}, 404)

    if request.method == 'PATCH':
        name = request.form.get('name')
        if name:
            bakery.name = name
            db.session.commit()
        response = make_response(bakery.to_dict(), 200)
    else:  # GET
        response = make_response(bakery.to_dict(), 200)
    
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(desc(BakedGood.price)).all()
    baked_goods_list = [baked_good.to_dict() for baked_good in baked_goods]
    response = make_response(baked_goods_list, 200)
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(desc(BakedGood.price)).first()
    if baked_good:
        response = make_response(baked_good.to_dict(), 200)
    else:
        response = make_response({"error": "No baked goods found"}, 404)
    return response

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    name = request.form.get('name')
    price = request.form.get('price')
    bakery_id = request.form.get('bakery_id')

    if not name or not price:
        return make_response({"error": "Name and price are required"}, 400)

    baked_good = BakedGood(name=name, price=float(price), bakery_id=bakery_id)
    db.session.add(baked_good)
    db.session.commit()

    response = make_response(baked_good.to_dict(), 201)
    return response

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.filter(BakedGood.id == id).first()

    if not baked_good:
        return make_response({"error": "Baked good not found"}, 404)

    db.session.delete(baked_good)
    db.session.commit()

    response = make_response({"message": f"Baked good with ID {id} successfully deleted."}, 200)
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)

if __name__ == '__main__':
    app.run(port=5555, debug=True)