import braintree

from flask import Flask
from flask_restful import reqparse, Resource, Api
app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('payment_method_nonce', type=str, help='required')
parser.add_argument('amount', type=str, help='The amount to pay')


braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id='zf39nyvdzr5y8666',
                                  public_key='6thc6f5vhx7m5d3y',
                                  private_key='62a678e1651db3435a4adb2220dd2251')


class Token(Resource):
    def get(self):
        try:
            return {'token': braintree.ClientToken.generate()}, 200
        except Exception:
            return '', 500


class Pay(Resource):
    def post(self):
        args = parser.parse_args(strict=True)
        result = braintree.Transaction.sale({
            "amount": args['amount'],
            "payment_method_nonce": args['payment_method_nonce'],
            "options": {
                "submit_for_settlement": True
            }
        })
        if result.is_success:
                return {'message': 'Payment done'}, 200
        return {'message': 'Error'}, 400

api.add_resource(Token, '/api/payments/token')
api.add_resource(Pay, '/api/payments/pay')


if __name__ == '__main__':
    app.run(debug=True)

