from flask import Flask
from flask_restful import Resource, Api, reqparse
import api_functions
import uuid
from multiprocessing import Process

app = Flask(__name__)
api = Api(app)

currentProcesses = dict()


class Bulbs(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('function', required=True)
        parser.add_argument('speed', required=True)
        args = parser.parse_args()

        p = Process(target=api_functions.rainbow_mode, args=(['7C78B214359E', '7C78B2172ED6',
                                                              '7C78B217887C', '7C78B2189C55', '7C78B2171F1F'],), daemon=True)

        id = str(uuid.uuid4())
        p.name = id
        currentProcesses[id] = p
        p.start()
        
        return {'data': {'success': True, 'pid': id}}, 200

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('pid', required=False)
        args = parser.parse_args()

        if args['pid'] is None: # If no pid received, terminate all processes
            for _, p in currentProcesses.items():
                p.terminate()
                p.join()
                del currentProcesses[args['pid']]
        elif args['pid'] in currentProcesses:
            p = currentProcesses[args['pid']]
            p.terminate()
            p.join()
            del currentProcesses[args['pid']]
        else:
            return {'data': 'Process Not Found'}, 404

        return {'data': 'Success'}, 200


api.add_resource(Bulbs, '/bulbs')  # add endpoints

if __name__ == '__main__':
    app.run()  # run our Flask app
