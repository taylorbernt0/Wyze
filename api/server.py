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
    'temp': api_functions.temp_mode,
    'color': api_functions.color_mode,
    'rainbow': api_functions.rainbow_mode,
    'party': api_functions.party_mode,
    'strobe': api_functions.strobe_mode
}

class Bulbs(Resource):
    def __init__(self):
        self.client = api_functions.get_client()

    def get(self):
        return app.response_class(
            response=api_functions.get_bulbs_info_json(self.client),
            status=200,
            mimetype='application/json'
        )

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('macs', required=False)
        parser.add_argument('mode', required=False)
        parser.add_argument('brightness', required=False)
        parser.add_argument('color', required=False)

        args = parser.parse_args()
        kwargs_list = {}

        macs = args['macs']
        mode = args['mode']
        brightness = args['brightness']
        color = args['color']

        try:
            # Validate mode arguments
            if (mode is None) or (mode not in mode_map):
                return {'data': 'Mode Name Not Found'}, 404
            elif mode == 'temp' and (macs is None or color is None):
                return {'data': 'Arguments required: (macs, color)'}, 404
            elif mode == 'color' and (macs is None or color is None):
                return {'data': 'Arguments required: (macs, color)'}, 404
            elif mode == 'rainbow' and (macs is None):
                return {'data': 'Arguments required: (macs)'}, 404
            elif mode == 'party' and (macs is None):
                return {'data': 'Arguments required: (macs)'}, 404
            elif mode == 'strobe' and (macs is None):
                return {'data': 'Arguments required: (macs)'}, 404

            # MACS
            macs = ast.literal_eval(macs)
            macs = [e.strip() for e in macs]

            # BRIGHTNESS
            if brightness is not None and ((not brightness.isdigit()) or (int(brightness) < 0) or (int(brightness) > 100)):
                return {'data': 'Invalid Brightness'}, 404
            elif brightness is not None:
                kwargs_list['brightness'] = int(brightness)

            # COLOR
            if color is not None:
                kwargs_list['color'] = color

            # Create mode process
            id = str(uuid.uuid4())
            p = Process(target=mode_map[mode], args=(self.client, macs,), kwargs=kwargs_list, daemon=True, name=id)
            currentProcesses[id] = p
            p.start()
        except:
            return {'data': 'Something Went Wrong :('}, 404
        
        return {'data': {'Success': True, 'pid': id}}, 200

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
