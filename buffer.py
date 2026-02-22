import json
import random

types = ["rectangle","circle","triangle","polygon","star","line",
         "cube","sphere","pyramid","prism","cone","cylinder","point"]

def generate_size(t):
    if t=="rectangle":
        return {"width": round(random.uniform(5,20),2),
                "height": round(random.uniform(5,20),2)}
    elif t=="circle":
        return {"radius": round(random.uniform(5,15),2)}
    elif t=="triangle":
        return {"base": round(random.uniform(5,20),2),
                "height": round(random.uniform(5,20),2)}
    elif t=="polygon":
        return {"sides": random.randint(3,8),
                "radius": round(random.uniform(5,15),2)}
    elif t=="star":
        return {"points": random.randint(5,10),
                "outer": round(random.uniform(5,15),2),
                "inner": round(random.uniform(2,7),2)}
    elif t=="line":
        return {"width": random.randint(1,5),
                "x0": random.randint(0,20),
                "y0": random.randint(0,20),
                "lineW": round(random.uniform(0.1,1),2)}
    elif t=="cube":
        return {"width": round(random.uniform(5,20),2),
                "height": round(random.uniform(5,20),2),
                "depth": round(random.uniform(5,20),2),
                "mode": random.choice([True, False])}
    elif t=="sphere":
        return {"radius": round(random.uniform(5,15),2),
                "slices": random.randint(8,32),
                "stacks": random.randint(8,32),
                "mode": random.choice([True, False])}
    elif t=="pyramid":
        return {}  # как в рабочем примере
    elif t=="prism":
        return {"sides": random.randint(3,8),
                "radius": round(random.uniform(5,15),2),
                "height": round(random.uniform(5,20),2),
                "mode": random.choice([True, False])}
    elif t=="cone":
        return {"radius": round(random.uniform(5,15),2),
                "h": round(random.uniform(5,20),2),
                "mode": random.choice([True, False])}
    elif t=="cylinder":
        return {"rTop": random.randint(5,15),
                "rBottom": round(random.uniform(5,15),2),
                "h": round(random.uniform(5,20),2),
                "mode": random.choice([True, False])}
    elif t=="point":
        return {"size": random.randint(5,20)}
    return {}

objects = []

for i in range(1000):
    t = random.choice(types)
    obj = {
        "color": {"r": round(random.random(), 2),
                  "g": round(random.random(), 2),
                  "b": round(random.random(), 2)},
        "name": f"figure{i}",
        "position": {"x": int(round(random.uniform(-300, 300), 2)),
                     "y": int(round(random.uniform(-300, 300), 2)),
                     "z": int(round(random.uniform(-300, 300), 2))},

        "size": generate_size(t),
        "type": t,
        "parent": "None",
    }
    objects.append(obj)

scene = {"mode":"3D","objects":objects}

with open("scene_100_working.json","w") as f:
    json.dump(scene,f,indent=4)

print("scene_100_working.json создан, должен импортироваться importScene")
