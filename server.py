import json

import numpy as np
from flask import Flask, request, jsonify
from flask_restful import Resource, Api

from distanceWO import Expert
from item2item import item2item

app = Flask(__name__)
api = Api(app)


class ExpertRequest(Resource):

    def post(self):
        print(request.data)
        full_json = json.loads(request.data)
        user_json = full_json['user']
        user_json["distance"][0] = -np.infty if user_json["distance"][0] == 1.4E-45 else user_json["distance"][0]
        user_json["distance"][1] = np.infty if user_json["distance"][1] == 3.4028235E38 else user_json["distance"][
            1]
        user_json["salary"][0] = -np.infty if user_json["salary"][0] == 1.4E-45 else user_json["salary"][0]
        user_json["salary"][1] = np.infty if user_json["salary"][1] == 3.4028235E38 else user_json["salary"][1]
        user_json["labour"][0] = -np.infty if user_json["labour"][0] == 1.4E-45 else user_json["labour"][0]
        user_json["labour"][1] = np.infty if user_json["labour"][1] == 3.4028235E38 else user_json["labour"][1]

        user = [
            (user_json["distance"][0], user_json["distance"][1]),
            (user_json["salary"][0], user_json["salary"][1]),
            (user_json["labour"][0], user_json["labour"][1]),
            user_json["remote"],
            [s for s in user_json["skills"]],
            user_json["pc"]
        ]

        offers_json = full_json['offers']
        offers = []
        for offer in offers_json:
            offers.append([(True if offer["remote"] == 1 else 0), offer["salary"], offer["labour"], [
                s for s in offer["skills"]], [s for s in offer["coords"]], offer["id"]])

        # await websocket.send(str(Expert(user, offers)))
        # await websocket.send(json.dumps(Expert(user, offers).tolist()))
        print("Sending back offer")
        return jsonify(Expert(user, offers).tolist())


class I2IOffer(Resource):

    def post(self):
        full_json = json.loads(request.data)
        user_json = full_json['user']
        user_json["distance"][0] = -np.infty if user_json["distance"][0] == 1.4E-45 else user_json["distance"][0]
        user_json["distance"][1] = np.infty if user_json["distance"][1] == 3.4028235E38 else user_json["distance"][
            1]
        user_json["salary"][0] = -np.infty if user_json["salary"][0] == 1.4E-45 else user_json["salary"][0]
        user_json["salary"][1] = np.infty if user_json["salary"][1] == 3.4028235E38 else user_json["salary"][1]
        user_json["labour"][0] = -np.infty if user_json["labour"][0] == 1.4E-45 else user_json["labour"][0]
        user_json["labour"][1] = np.infty if user_json["labour"][1] == 3.4028235E38 else user_json["labour"][1]

        user = [
            (user_json["distance"][0], user_json["distance"][1]),
            (user_json["salary"][0], user_json["salary"][1]),
            (user_json["labour"][0], user_json["labour"][1]),
            user_json["remote"],
            [s for s in user_json["skills"]],
            user_json["pc"]
        ]

        liked_json = full_json['liked']
        liked = []
        for offer in liked_json:
            liked.append([(True if offer["remote"] == 1 else 0), offer["salary"], offer["labour"], [
                s for s in offer["skills"]], [s for s in offer["coords"]], offer["id"]])

        offers_json = full_json['offers']
        offers = []
        for offer in offers_json:
            offers.append([(True if offer["remote"] == 1 else 0), offer["salary"], offer["labour"], [
                s for s in offer["skills"]], [s for s in offer["coords"]], offer["id"]])

        # await websocket.send(str(item2item(user, liked, offers)))
        # await websocket.send(json.dumps({'offer': offer}))
        return jsonify(item2item(user, liked, offers).tolist())


api.add_resource(ExpertRequest, '/expert')
api.add_resource(I2IOffer, '/i2ioffer')

if __name__ == '__main__':
    app.run(port=4321)
