import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import struct
import numpy as np
import math

app = dash.Dash(__name__)

G = 6.67 * pow(10, -11)  # gravitational constant

#generowanie strony

app.layout = html.Div([
    html.H1("Symulacja lądowania rakiety na Marsie"),

    html.Label("Czas sygnału:"),
    dcc.Slider(
        id='t-step-slider',
        min=0.25,
        max=2,
        step=0.25,
        marks={0.0: '0.0', 0.25: '0.25', 0.5: '0.5', 0.75: '0.75', 1: '1', 1.25: '1.25', 1.5: '1.5', 1.75: '1.75', 2: '2'},
        value=0.5
    ),

    html.Label("Prędkość początkowa:"),
    dcc.Slider(id='v-start-slider', min=0, max=100, step=10, marks={i: str(i) for i in range(0, 101, 10)}, value=10),

    html.Label("Wyskość początkowa:"),
    dcc.Slider(id='h-start-slider', min=1000, max=20000, step=1000, marks={i: str(i) for i in range(0, 20001, 1000)}, value=7000),

    html.Div(id='landed?'),
    html.Div("Prędkość w momencie około zetknięcia z powierzchnią:"),
    html.Div(id='vCurr'),
    html.Div("siła uderzenia:"),
    html.Div(id='impact_force'),

    html.Div([
        dcc.Graph(id='height-graph'),
        dcc.Graph(id='velocity-graph'),
    ], style={'display': 'flex'}),

    html.Div([
        dcc.Graph(id='acceleration-graph'),
        dcc.Graph(id='thrust-graph'),
    ], style={'display': 'flex'}),
])

@app.callback(
    [Output(component_id='landed?', component_property='children'),
    Output(component_id='vCurr', component_property='children'),
    Output(component_id='impact_force', component_property='children'),
    Output('height-graph', 'figure'),
     Output('velocity-graph', 'figure'),
     Output('acceleration-graph', 'figure'),
     Output('thrust-graph', 'figure')],
    [Input('t-step-slider', 'value'),
     Input('v-start-slider', 'value'),
     Input('h-start-slider', 'value')]
)
# symulacja

def run_simulation(t_step, vStart, hStart):
    def should_launch_thrust():
        sim_with_thrust_1 = struct.unpack('ffff', time_to_reach_ground(1))
        sim_with_thrust_05 = struct.unpack('ffff', time_to_reach_ground(0.5))
        sim_with_thrust_025 = struct.unpack('ffff', time_to_reach_ground(0.25))
        sim_without_thrust = struct.unpack('ffff', time_to_reach_ground(0))

        # print("t:", t, "\nwith th:", sim_with_thrust, "\nwithout:", sim_without_thrust)

        if sim_with_thrust_1[1] - vCurr * (t_step + 1) < 0:
            return 1
        elif sim_with_thrust_05[1] - vCurr * (t_step + 1) < 0 and hCurr < 1000:
            return 0.5
        elif sim_with_thrust_025[1] - vCurr * (t_step + 1) < 0 and hCurr < 500:
            return 0.25

        return 0

    def time_to_reach_ground(thrust):
        time = -t_step

        a_temp = - Tmax * thrust / Ms + g

        v_temp = vCurr + a_temp * t_step
        h_temp = hCurr - v_temp * t_step

        while h_temp >= 0 and v_temp >= 0:
            v_temp += a_temp * t_step
            h_temp -= v_temp * t_step

            time += t_step

        # 1 tick more, to be ahead of crush and prefent it. It will couse oscilations.

        var = struct.pack('ffff', time, h_temp, v_temp, a_temp)
        return var

    G = 6.67 * pow(10, -11)  # stała grawitacyjna

    tSimEnd = 1000
    t = 0

    Ms = 1000  # masa łazika
    Mp = 6.41 * pow(10, 23)  # masa planety
    Rp = 3389000  # km promien
    g = G * Mp / (Rp * Rp)  # grawitacja planety

    hCurr = hStart
    vCurr = vStart
    aCurr = g
    thr = 0

    max_impact_force = 2000

    Tmax = 15000  # N maksymalna przepustnica
    Fmax = - Tmax / Ms + g

    # tablice dla wykresów
    dt = []
    h = []
    v = []  # na plusie, gdy spada
    a = []
    thrust_applied = []

    while t < tSimEnd:

        dt.append(t)

        a.append(aCurr)
        v.append(vCurr)
        h.append(hCurr)
        thrust_applied.append(thr)

        thr = should_launch_thrust()
        print(aCurr, "t:", t, "h:", hCurr, "v:", vCurr, "applying thrust:", should_launch_thrust())
        aCurr = thr * -Tmax / Ms + g

        hCurr -= vCurr * t_step + 1/2*aCurr*t_step*t_step
        vCurr += aCurr * t_step
        t += t_step
        if hCurr <= 0:
            if v[-1] > 0:
                v_final = v[-1]
            if vCurr > 0:
                v_final=vCurr
            impact_force = Ms * v_final
            if impact_force > max_impact_force:
                print("Rakieta rozbiła się")
                crush_check="Rakieta rozbiła się"
            else:
                print("Rakieta wylądowała!")
                crush_check = "Rakieta wylądowała!"
                v_final = round(v_final, 2)
                impact_force = round(impact_force, 2)
            print(aCurr, "With speed:", v_final, "height", hCurr, "and impact force of:", impact_force)

            break
    # Your existing simulation code here...
    # ... (Copy the entire simulation code here and modify as needed)

    # Return the updated figures for each graph
    return crush_check, f'{v_final} [m/s]', f'{impact_force} [N]', *generate_figures(dt,h,v,a, thrust_applied)

def generate_figures(dt, h, v, a, thrust_applied):
    fig_height = plt_to_dash(dt, h, "Wysokość", "Czas [s]", "Wysokość [m]")
    fig_velocity = plt_to_dash(dt, v, "Prędkość", "Czas [s]", "Prędkość [m/s]")
    fig_acceleration = plt_to_dash(dt, a, "Przyspieszenie", "Czas [s]", "Przyspieszenie [m/s^2]")
    fig_thrust = plt_to_dash(dt, thrust_applied, "Ciąg", "Czas [s]", "Siła ciągu [N]")

    return fig_height, fig_velocity, fig_acceleration, fig_thrust

def plt_to_dash(x, y, title, x_label, y_label):
    return {
        'data': [{'x': x, 'y': y, 'type': 'line', 'name': 'line'}],
        'layout': {'title': title, 'xaxis': {'title': x_label}, 'yaxis': {'title': y_label}}
    }

if __name__ == '__main__':
    app.run_server(debug=True)