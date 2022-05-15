import numpy as np
import math

from GeoUtils import GeoUtils
from distanceWO import branches, unique_list


def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def normalize(v, min=0, max=10):
    return (v - min) / (max - min)


def item2item(user, liked, items):
    def vectorize_skill(skills):
        n_skills = len(unique_list)
        l = unique_list
        v = np.zeros(n_skills)

        for skill in skills:
            for b in branches:
                for ski in b[0]:
                    if ski == skill:
                        v[l.index(ski)] = 1
                    elif skill in b[0]:
                        v[l.index(ski)] = max(b[1], v[l.index(ski)])
        return v

    v_u = vectorize_skill(user[4])

    def vectorize_item(item):
        offer = item
        v_t = np.zeros(6)
        # Calculate Distance puntuation
        pc = str(user[5])
        if len(pc) < 5:
            pc = "0" * (5 - len(pc)) + pc
        lat1, lon1 = offer[4][0], offer[4][1]
        lat2, lon2 = GeoUtils.get_coords_from_postal_code(pc)
        dist = GeoUtils.get_distance(lat1, lon1, lat2, lon2)
        if dist < user[0][0] or dist > user[0][1]:
            v_t[0] = - min(abs(dist - user[0][0]), abs(dist - user[0][1])) / 20
        else:
            aux = dist - user[0][0]
            aux = aux / (user[0][1] - user[0][0])
            r = 0
            if aux == 0:
                r = 1
            else:
                r = 1 - aux * 0.5
            if math.isnan(r):
                r = 1.5
            v_t[0] = r

        # Calculate Salary puntuation
        if offer[1] < user[1][0]:
            v_t[1] = - min(abs(offer[1] - user[1][0]), abs(offer[1] - user[1][1])) / 2000
        else:
            aux = user[1][1] - offer[1]
            aux = aux / (user[1][1] - user[1][0])
            r = 0
            if aux == 0:
                r = 1
            else:
                r = 1 - aux * 0.5
            if math.isnan(r):
                r = 1.5
            v_t[1] = min(r, 1.5)

        v_t[2] = 0.0 if offer[2] < user[2][0] or offer[0] > user[2][1] else 1.0

        v_t[3] = 0.0 if offer[0] and user == 1 else 1.0

        p = vectorize_skill(offer[3])
        inds = np.where(p == 1)
        v_o = np.zeros_like(p)
        v_o[inds] = 1

        inds = np.where(v_o != 1)
        v_c = np.copy(v_u)
        v_c[inds] = 0
        v_t[4] = cosine_similarity(v_c, v_o)
        v_t[5] = offer[5]
        return v_t

    vectorized_likeds = []
    for like in liked:
        vectorized_likeds.append(vectorize_item(like))

    vectorized_offers = []
    for item in items:
        vectorized_offers.append(vectorize_item(item))

    compatibility = []
    for v_o in vectorized_offers:
        aux = np.where(v_o == 1)
        compatibility.append((sum([cosine_similarity(v_o[:-1], v_l[:-1]) for v_l in vectorized_likeds])/len(vectorized_likeds), v_o[5]))
    compatibility.sort(key=lambda x: x[0], reverse=True)
    print(compatibility)
    return np.array(compatibility)[:, 1].astype(int)
    pass
