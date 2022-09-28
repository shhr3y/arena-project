import eventlet
import socketio
import json
import dataclasses
from typing import List, Mapping, Optional, Tuple, Union
import mediapipe as mp
import plotly.express as px
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import dash
from dash import html
from dash import dcc


host = '192.168.0.103'
port = 9876	

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

_PRESENCE_THRESHOLD = 0.5
_VISIBILITY_THRESHOLD = 0.5

sio = socketio.Server(cors_allowed_origins="*", async_mode='eventlet')
app = socketio.WSGIApp(sio)


# def ping_in_intervals():
#     threading.Timer(5.0, ping_in_intervals).start()
#     print("send ping")
#     sio.emit('ping')


@sio.on('landmarks')
def ping(*args):
    landmarks = args[1]
    json_list = []
    for landmark in landmarks:
        json_object = json.loads(landmark)
        json_list.append(json_object)

    fig.update(plot_landmarks(json_list,  mp_pose.POSE_CONNECTIONS))





fig = go.Figure()

def plot_landmarks(landmark_list, connections=None):
    if not landmark_list:
        return
    
    plotted_landmarks = {}
    for idx, landmark in enumerate(landmark_list):
        if (landmark['visibility'] < _VISIBILITY_THRESHOLD) or (landmark['presence'] < _PRESENCE_THRESHOLD):
            continue

        plotted_landmarks[idx] = (-landmark['z'], landmark['x'], -landmark['y'])
    if connections:
        out_cn = []
        num_landmarks = len(landmark_list)
        # Draws the connections if the start and end landmarks are both visible.
        for connection in connections:
            start_idx = connection[0]
            end_idx = connection[1]
            if not (0 <= start_idx < num_landmarks and 0 <= end_idx < num_landmarks):
                raise ValueError(
                    f"Landmark index is out of range. Invalid connection "
                    f"from landmark #{start_idx} to landmark #{end_idx}."
                )
            if start_idx in plotted_landmarks and end_idx in plotted_landmarks:
                landmark_pair = [
                    plotted_landmarks[start_idx],
                    plotted_landmarks[end_idx],
                ]
                out_cn.append(
                    dict(
                        xs=[landmark_pair[0][0], landmark_pair[1][0]],
                        ys=[landmark_pair[0][1], landmark_pair[1][1]],
                        zs=[landmark_pair[0][2], landmark_pair[1][2]],
                    )
                )
            
        cn2 = {"xs": [], "ys": [], "zs": []}
        for pair in out_cn:
            for k in pair.keys():
                cn2[k].append(pair[k][0])
                cn2[k].append(pair[k][1])
                cn2[k].append(None)

    df = pd.DataFrame(plotted_landmarks).T.rename(columns={0: "z", 1: "x", 2: "y"})
    df["lm"] = df.index.map(lambda s: mp_pose.PoseLandmark(s).name).values
    figure = (
        px.scatter_3d(df, x="z", y="x", z="y", hover_name="lm")
        .update_traces(marker={"color": "red"})
        .update_layout(
            margin={"l": 0, "r": 0, "t": 0, "b": 0},
            scene={"camera": {"eye": {"x": 2.1, "y": 0, "z": 0}}},
        )
    )
    figure.add_traces(
        [
            go.Scatter3d(
                x=cn2["xs"],
                y=cn2["ys"],
                z=cn2["zs"],
                mode="lines",
                line={"color": "black", "width": 5},
                name="connections",
            )
        ]
        )
    return figure

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])
    
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
    eventlet.wsgi.server(eventlet.listen((host, port)), app)
