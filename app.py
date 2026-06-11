import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)

devices = pd.read_csv("data/devices.csv")

from network_monitor import ping_device

devices["Status"] = devices["IP"].apply(ping_device)

# KPI calculations
online_devices = len(devices[devices["Status"] == "Online"])
offline_devices = len(devices[devices["Status"] == "Offline"])
avg_latency = round(devices["Latency"].mean(), 1)

# Create charts
status_counts = devices["Status"].value_counts()

pie_fig = px.pie(
    values=status_counts.values,
    names=status_counts.index,
    title="Device Status"
)

latency_fig = px.bar(
    devices,
    x="Device",
    y="Latency",
    title="Network Latency (ms)"
)

status_counts = devices["Status"].value_counts()

pie_fig = px.pie(
    values=status_counts.values,
    names=status_counts.index,
    title="Device Status"
)

latency_fig = px.bar(
    devices,
    x="Device",
    y="Latency",
    title="Network Latency (ms)"
)

table_rows = []

for _, row in devices.iterrows():
    table_rows.append
    html.Tr([
            html.Td(row["Device"]),
            html.Td(row["IP"]),
            html.Td(row["Status"]),
            html.Td(f'{row["Latency"]} ms')
        ])
    

app.layout = html.Div([

    html.H1(
        "Smart Campus Network Monitoring System",
        style={"textAlign": "center"}
    ),

    dcc.Interval(
        id="refresh",
        interval=30*1000,
        n_intervals=0
    ),

    html.Div([

        html.Div([
            html.H3("Online Devices"),
            html.H2(str(online_devices))
        ], className="card"),

        html.Div([
            html.H3("Offline Devices"),
            html.H2(str(offline_devices))
        ], className="card"),

        html.Div([
            html.H3("Average Latency"),
            html.H2(f"{avg_latency} ms")
        ], className="card")

    ], className="cards"),

    html.H2("Network Devices"),

    html.Table([
        html.Tr([
            html.Th("Device"),
            html.Th("IP Address"),
            html.Th("Status"),
            html.Th("Latency")
        ])
    ] + table_rows),

    dcc.Graph(figure=pie_fig),

    dcc.Graph(figure=latency_fig),

    html.Pre("""
            Internet
                |
          Main Router
          /         \\
 Library SW      Faculty SW
      |              |
 Student AP     Hostel AP
    """)

])
if __name__ == "__main__":
    app.run(debug=True)