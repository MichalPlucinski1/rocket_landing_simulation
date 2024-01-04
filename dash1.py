import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import struct

app = dash.Dash(__name__)

G = 6.67 * pow(10, -11)  # gravitational constant

app.layout = html.Div([
    html.H1("Rocket Simulation Dash App"),

    html.Label("Time Step (t_step):"),
    dcc.Input(id='t-step-input', type='number', value=0.5),

    html.Label("Initial Velocity (vStart):"),
    dcc.Input(id='v-start-input', type='number', value=10),

    html.Label("Initial Height (hStart):"),
    dcc.Input(id='h-start-input', type='number', value=7000),

    html.Button('Run Simulation', id='run-button'),

    dcc.Graph(id='height-graph'),
    dcc.Graph(id='velocity-graph'),
    dcc.Graph(id='acceleration-graph'),
    dcc.Graph(id='thrust-graph')
])

@app.callback(
    [Output('height-graph', 'figure'),
     Output('velocity-graph', 'figure'),
     Output('acceleration-graph', 'figure'),
     Output('thrust-graph', 'figure')],
    [Input('run-button', 'n_clicks')],
    [Input('t-step-input', 'value'),
     Input('v-start-input', 'value'),
     Input('h-start-input', 'value')]
)

def run_simulation(n_clicks, t_step, vStart, hStart):
    def should_launch_thrust():
        sim_with_thrust_1 = struct.unpack('ffff', time_to_reach_ground(1))
        sim_with_thrust_05 = struct.unpack('ffff', time_to_reach_ground(0.5))
        sim_with_thrust_025 = struct.unpack('ffff', time_to_reach_ground(0.25))
        sim_without_thrust = struct.unpack('ffff', time_to_reach_ground(0))

        # print("t:", t, "\nwith th:", sim_with_thrust, "\nwithout:", sim_without_thrust)

        if sim_with_thrust_1[1] - vCurr < 0:
            return 1
        elif sim_with_thrust_05[1] - vCurr < 0 and hCurr < 1000:
            return 0.5
        elif sim_with_thrust_025[1] - vCurr < 0 and hCurr < 500:
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


    tSimEnd = 300
    #czas miedzy pomiarami
    t = 0

    Ms = 1000  # masa łazika
    Mp = 6.41 * pow(10, 23)  # masa planety
    Rp = 3389000  # km promien
    g = G * Mp / (Rp * Rp)  # grawitacja planety

    hCurr = hStart
    vCurr = vStart
    aCurr = g
    thr = 0

    Tmax = 15000  # N maksymalna przepustnica
    Fmax = - Tmax / Ms + g

    #tablice dla wykresów
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
        aCurr = thr * -Tmax / Ms + g
        print("t:", t, "h:", hCurr, "applying thrust:", should_launch_thrust())

        vCurr += aCurr * t_step
        hCurr -= vCurr * t_step

        t += t_step

        if hCurr <= 0 and vCurr > 10:
            print("crash at speed", vCurr)
            break
        else:
            if hCurr <= 0:
                print("Landed! at speed", vCurr)
                break
    # Your existing simulation code here...
    # ... (Copy the entire simulation code here and modify as needed)

    # Return the updated figures for each graph
    return generate_figures(dt,h,v,a, thrust_applied)

def generate_figures(dt, h, v, a, thrust_applied):
    fig_height = plt_to_dash(dt, h, "Wysokość", "Czas [s]", "Wysokość [m]")
    fig_velocity = plt_to_dash(dt, v, "Prędkość", "Czas [s]", "v")
    fig_acceleration = plt_to_dash(dt, a, "Przyspieszenie", "Czas [s]", "a")
    fig_thrust = plt_to_dash(dt, thrust_applied, "Ciąg", "Czas [s]", "thr")

    return fig_height, fig_velocity, fig_acceleration, fig_thrust

def plt_to_dash(x, y, title, x_label, y_label):
    return {
        'data': [{'x': x, 'y': y, 'type': 'line', 'name': 'line'}],
        'layout': {'title': title, 'xaxis': {'title': x_label}, 'yaxis': {'title': y_label}}
    }

if __name__ == '__main__':
    app.run_server(debug=True)
