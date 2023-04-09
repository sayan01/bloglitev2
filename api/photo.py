# take photo from form data and save in filesystem then return the path
from flask import request
from flask_restful import Resource, fields, marshal_with, reqparse, marshal, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
import uuid
from api import api

photo_fields = {
    'path': fields.String,
}

photo_parser = reqparse.RequestParser()
photo_parser.add_argument('photo', type=FileStorage, location='files', required=True)

class PhotoUpload(Resource):
    @jwt_required()
    @marshal_with(photo_fields)
    def post(self):
        print(request.files)
        args = photo_parser.parse_args()
        photo = args['photo']
        filename = secure_filename(photo.filename)
        # if file is not image, abort
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            print('File must be an image')
            abort(400, message='File must be an image')
        # if file is too large, abort
        if len(photo.read()) > 1024 * 1024:
            print('File must be less than 1MB')
            abort(400, message='File must be less than 1MB')
        
        # if static/photos directory does not exist, create it
        if not os.path.exists(os.path.join('static', 'photos')):
            os.makedirs(os.path.join('static', 'photos'))

        userid = get_jwt_identity()
        path = os.path.join('static', 'photos', f'{userid}-{uuid.uuid4()}-{filename}')
        photo.seek(0)
        photo.save(path)
        return {'path': path}, 201

api.add_resource(PhotoUpload, '/photo')