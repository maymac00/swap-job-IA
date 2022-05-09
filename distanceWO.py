import numpy as np
from GeoUtils import GeoUtils

branches = [
    ({"C++", "C", "C#", "Visual Studio"}, 0.8),
    ({"C++", "Python", "Java", "C", "C#"}, 0.5),
    ({"JavaScript", "Node.js", "React", "React Native", "Angular", "Vue", "Django", "Flask", "Typescript"},
     0.3),
    ({"Java", "JavaScript", "Junit"}, 0.6),
    ({"SQL", "Express", "MongoDB", "MySQL", "PostgreSQL", "SQLite"}, 0.25),
    ({"Data Science", "Data Mining", "Data Analysis", "Business Intelligence"}, 0.7),
    ({"Data Engineering", "Data Warehousing"}, 0.9),
    ({"Data Warehousing", "SAP", "CRM", "ERP Systems", "Business Intelligence"}, 0.25),
    ({"Firebase", "Firebase Hosting", "CRM", "ERP Systems"}, 0.25),
    ({"Machine Learning", "Data Science", "Data Visualization", "Data Analysis", "Data Mining", "Data Engineering",
      "Data Warehousing"}, 0.25),
    ({"Git", "GitHub", "GitLab", "GitKraken", "GitFlow", "GitHub Pages"}, 0.9),
    ({"Agile Development", "Scrum", "Kanban", "REST"}, 0.5),
    ({"Jest", "JUnit", "Selenium", "Jasmine"}, 0.4),
    ({"ASP.NET", "C#", ".NET"}, 0.8),
    ({"Unity", "Unreal"}, 0.5),
    # esta estructura estaria bien tenerla siempre cargada en el servidor así no hay que crearla cada vez
]

unique_set = set()
for s in branches:
    unique_set = unique_set.union(s[0])
unique_list = list(unique_set)


def Expert(user, offer):
    puntuation = np.zeros(
        5)  # Vector para la puntacion de los diferentes parametros (Distance, Salary, Labour, Remote, Skills)

    # Calculate Distance puntuation
    pc = str(user[5])
    if len(pc) < 5:
        pc = "0" * (5 - len(pc)) + pc
    lat1, lon1 = offer[4][0], offer[4][1]
    lat2, lon2 = GeoUtils.get_coords_from_postal_code(pc)
    dist = GeoUtils.get_distance(lat1, lon1, lat2, lon2)
    if dist < user[0][0] or dist > user[0][1]:
        puntuation[0] = - min(abs(dist - user[0][0]), abs(dist - user[0][1])) / 20
    else:
        aux = dist - user[0][0]
        aux = aux / (user[0][1] - user[0][0])
        r = 0
        if aux == 0:
            r = 1
        else:
            r = 1 - aux * 0.5
        puntuation[0] = r

    # Calculate Salary puntuation
    if offer[1] < user[1][0]:
        puntuation[1] = - min(abs(offer[1] - user[1][0]), abs(offer[1] - user[1][1])) / 2000
    else:
        aux = user[1][1] - offer[1]
        aux = aux / (user[1][1] - user[1][0])
        r = 0
        if aux == 0:
            r = 1
        else:
            r = 1 - aux * 0.5
        puntuation[1] = min(r, 1.5)
    # Calculate Labour puntuation (min: 0, max 1)
    puntuation[2] = 0.0 if offer[2] < user[2][0] or offer[0] > user[2][1] else 1.0

    # Calculate Remote puntuation (min: 0, max 1)
    puntuation[3] = 0.0 if offer[0] and user == 1 else 1.0

    # Calculate Skills puntuation
    # Skills, compatibility

    p = 0
    for skill in offer[3]:
        for u_skill in user[4]:
            if skill == u_skill:
                p += 1
                break
            aux = 0
            for branch in branches:
                if skill in branch[0] and u_skill in branch[0]:
                    aux = max(branch[1], aux)
            p += aux

    puntuation[4] = p / len(offer[3])
    print(puntuation, sum(puntuation) * 2)
    return sum(puntuation) * 2  # La ponemos del 0 al 10
