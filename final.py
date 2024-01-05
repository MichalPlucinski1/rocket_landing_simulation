import matplotlib.pyplot as plt
import struct


def should_launch_thrust():
    sim_with_thrust_1 = struct.unpack('ffff', time_to_reach_ground(1))
    sim_with_thrust_05 = struct.unpack('ffff', time_to_reach_ground(0.5))
    sim_with_thrust_025 = struct.unpack('ffff', time_to_reach_ground(0.25))
    sim_without_thrust = struct.unpack('ffff', time_to_reach_ground(0))

    # print("t:", t, "\nwith th:", sim_with_thrust, "\nwithout:", sim_without_thrust)
    print(sim_with_thrust_1)

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


if __name__ == '__main__':

    G = 6.67 * pow(10, -11)  # stała grawitacyjna


    tSimEnd = 1000
    t_step = 0.5    #czas miedzy pomiarami
    t = 0
    hStart = 6000 # wysokosc poczatkowa
    vStart = 10  # predkosc m/s poczatkowa, dodatnia gdy zbliza się



    Ms = 1000  # masa łazika
    Mp = 6.41 * pow(10, 23)  # masa planety
    Rp = 3389000  # km promien
    g = G * Mp / (Rp * Rp)  # grawitacja planety

    max_impact_force = 500

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
        print("t:", t, "h:", hCurr, "applying thrust:", thr)

        vCurr += aCurr * t_step
        hCurr -= vCurr * t_step

        t += t_step

        if hCurr <= 0:
            impact_force = vCurr * Ms
            if impact_force > max_impact_force:
                print("Crush!")
            else:
                print("Landed!")
            print("With speed:",vCurr,"and impact force of:",impact_force)

            break

    plt.subplot(1, 4, 1)
    plt.plot(dt, h)
    plt.title("Wysokość")
    plt.xlabel("Czas [s]")
    plt.ylabel("Wysokość [m]")
    plt.grid(True)

    #
    plt.subplot(1, 4, 2)
    plt.plot(dt, v)
    plt.title("prędkość")
    plt.xlabel("Czas [s]")
    plt.ylabel("v")
    plt.grid(True)

    plt.subplot(1, 4, 3)
    plt.plot(dt, a)
    # plt.legend(["u_pi", "u"])
    plt.title("przyspieszenie")
    plt.xlabel("Czas [s]")
    plt.ylabel("a")
    plt.grid(True)

    plt.subplot(1, 4, 4)
    plt.plot(dt, thrust_applied)
    # plt.legend(["u_pi", "u"])
    plt.title("ciąg")
    plt.xlabel("Czas [s]")
    plt.ylabel("thr")
    plt.grid(True)

    plt.show()
