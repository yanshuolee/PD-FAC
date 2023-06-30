from itertools import product
from scipy.spatial.transform import Rotation as scipyR
from scipy.spatial import distance
import pandas as pd
import pickle

def generate_subgoal_coord_uav(angle=60):
    subg = []
    for ang in range(0, 360, angle):
        a = scipyR.from_euler('xyz', [0, 0, ang], degrees=True).as_quat()
        subg.append(tuple(a))
    return subg

w=8;h=8;l=8;stride=3
w_range, h_range, l_range = [i for i in range(0, w, stride)], \
    [i for i in range(0, h, stride)], [i for i in range(1, l, stride)]
subgoal_set = [i+j for i in product(w_range, h_range, l_range) for j in generate_subgoal_coord_uav()]

adj = distance.cdist(subgoal_set, subgoal_set, 'euclidean')

df = {
    "From":[],
    "To":[],
    "Cost":[]
}
for i in range(adj.shape[0]):
    for j in range(adj.shape[1]):
        df["From"].append(i)
        df["To"].append(j)
        df["Cost"].append(adj[i][j])

df = pd.DataFrame(df)
df.to_csv("./maps/empty_network.csv", index=False)

with open("./maps/empty_network_coord.pickle",
            'wb') as f:
    pickle.dump(subgoal_set, f)