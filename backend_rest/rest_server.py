from flask import Flask
from flask_restful import Resource, Api, reqparse
import werkzeug
import os.path

from tinydb import TinyDB, where, Query


db = TinyDB('testapp_db.json')
BIndex = Query()
results = db.search(BIndex.index_flag == 1)
if len(results) == 0:
    db.insert({'index_flag':1, 'biggest_index':1})


app = Flask(__name__)
api = Api(app)


class RESTServer(Resource):
    def get(self):
        return {}
    def get_biggest_index(self):
        BIndex = Query()
        global db
        results = db.search(BIndex.index_flag == 1)
        if len(results) == 0:
            return -1
        return results[0]['size']
    def increment_biggest_index(self):
        BIndex = Query()
        global db
        results = db.search(BIndex.index_flag == 1)
        if len(results) == 0:
            return
        current_index = results[0]['size']
        db.update({'size': current_index+1}, BIndex.index_flag == 1)
        
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        test_file = args['file']

        global biggest_index
        global db
        
        cur_index = self.get_biggest_index()
        self.increment_biggest_index()
        
        test_file.save("store/file{}".format(cur_index))
        db.insert({'id':cur_index, 'status':0})
        return {'id':cur_index}


class GetStatus(Resource):
    def get(self, id):
        if os.path.isfile("store/file{}".format(id)):
            return {'status': 'NotDone'}
        elif not os.path.isfile("store/res/output{}".format(id)):
            return {'status': 'DoesNotExist'}
        else:
            output_data = ""
            with open("store/res/output{}".format(id)) as output_file:
                output_data = output_file.read()
            return {'status': 'Done', 'content': output_data}
    
api.add_resource(RESTServer, '/')
api.add_resource(GetStatus, '/status/<id>')


if __name__ == '__main__':
    app.run(debug=True)


