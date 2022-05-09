import asyncio
import datetime

import numpy as np
import websockets
import json
from distanceWO import Expert
from item2item import item2item


async def time(websocket, path):
    if path == '/getExpert_offers':
        async for message in websocket:
            # print(message)
            full_json = json.loads(message)
            user_json = full_json['user']
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
                if "E" in offer["salary"][0]:
                    if "E-" in offer["salary"][0]:
                        offer["salary"][0] = -np.infty
                    else:
                        offer["salary"][0] = np.infty
                if "E" in offer["salary"][1]:
                    if "E-" in offer["salary"][1]:
                        offer["salary"][1] = -np.infty
                    else:
                        offer["salary"][1] = np.infty
                if "E" in offer["distance"][0]:
                    if "E-" in offer["distance"][0]:
                        offer["distance"][0] = -np.infty
                    else:
                        offer["distance"][0] = np.infty
                if "E" in offer["distance"][1]:
                    if "E-" in offer["distance"][1]:
                        offer["distance"][1] = -np.infty
                    else:
                        offer["distance"][1] = np.infty

                offers.append([(True if offer["remote"] == 1 else 0), offer["salary"], offer["labour"], [
                    s for s in offer["skills"]], [s for s in offer["coords"]]])

            await websocket.send(str([Expert(user, offer) for offer in offers]))
            # await websocket.send(json.dumps({'offer': offer}))
        print("offer received")

    if path == '/getI2I_offers':
        async for message in websocket:
            # print(message)
            full_json = json.loads(message)
            user_json = full_json['user']
            user_json["distance"][0] = -np.infty if user_json["distance"][0] == 1.4E-45 else user_json["distance"][0]
            user_json["distance"][1] = np.infty if user_json["distance"][1] == 3.4028235E38 else user_json["distance"][1]
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

            await websocket.send(str(item2item(user, liked, offers)))
            # await websocket.send(json.dumps({'offer': offer}))
        print("offer received")

    if path == '/base':
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        await websocket.send(now)
        await asyncio.sleep(1)
        d = {'first_name': 'Guido',
             'second_name': 'Rossum',
             'titles': ['BDFL', 'Developer'],
             }
        parsed = json.dumps(d)
        name = "Jeremy"
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        for i in range(1):
            await websocket.send(parsed)
            response = await websocket.recv()
            print(response)


start_server = websockets.serve(time, '127.0.0.1', 4321)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
