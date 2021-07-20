from flask import Flask
from flask_restful import Resource, Api, reqparse
import api_functions
import uuid
import ast
from multiprocessing import Process

app = Flask(__name__)
api = Api(app)

currentProcesses = dict()

mode_map = {
    'rainbow': api_functions.rainbow_mode,
    'party': api_functions.party_mode,
    'strobe': api_functions.strobe_mode
}

class Bulbs(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('macs', required=True)
        parser.add_argument('mode', required=True)
        parser.add_argument('brightness', required=True)
        parser.add_argument('speed', required=False)
        args = parser.parse_args()

        macs = ast.literal_eval(args['macs'])
        macs = [e.strip() for e in macs]

        mode = args['mode']
        if (mode is None) or (mode not in mode_map):
            return {'data': 'Mode Name Not Found'}, 404

        brightness = args['brightness']
        if (brightness is None) or (not isinstance(brightness, int) or (brightness < 0) or (brightness > 100)):
            return {'data': 'Invalid Brightness'}, 404

        p = Process(target=mode_map[mode], args=(macs,), kwargs={'brightness': brightness}, daemon=True)

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
            for id, p in currentProcesses.items():
                p.terminate()
                p.join()
            currentProcesses.clear()
        elif args['pid'] in currentProcesses:
            p = currentProcesses[args['pid']]
            p.terminate()
            p.join()
            del currentProcesses[args['pid']]
        else:
            return {'data': 'Process Id Not Found'}, 404

        return {'data': 'Success'}, 200


api.add_resource(Bulbs, '/bulbs')  # add endpoints

if __name__ == '__main__':
    app.run()  # run our Flask app
