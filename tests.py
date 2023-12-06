import math

import matplotlib.pyplot as plt


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def time_to_reach_distance_num(h, v, a):
    if v < 0:
        return -1

    time = 1
    timestamp = 1
    while h >= 0:
        v += a * timestamp
        h -= v * timestamp

        time += timestamp
    return time

def time_to_reach_distance_an(h, v, a):
    return math.sqrt(2 * (h - v * a) / a)

def F(velocity, distance):
    # Required to be thrust to land safely
    if distance <= 0:
        return 0  # If distance is 0 or negative, no thrust is needed (already landed)
    else:
        required_thrust = Ms * (velocity ** 2) / (2 * distance)
        return required_thrust  # Limit thrust to maximum 1500 Newtons


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    G = 6.67 * pow(10, -11)  # stała grawitacyjna

    # timestamp = 5  # czas miedzy pomiarami
    tSimEnd = 1500
    t_step = 1
    t = 0
    hStart = 10000  # wysokosc poczatkowa
    vStart = 10  # predkosc m/s poczatkowa, dodatnia gdy zbliza się

    Ms = 1000  # masa łazika
    Mp = 6.41 * pow(10, 23)  # masa planety
    Rp = 3389000  # km promien
    g = G * Mp / (Rp * Rp)  # grawitacja planety

    hCurr = hStart
    vCurr = vStart
    aCurr = g

    Fmax = 15000  # N maksymalna przepustnica
    Fcurr = 0  # obecna przepustnica

    time_to_distance_num = time_to_reach_distance_num(hStart, vCurr, aCurr)
    time_to_distance_an = time_to_reach_distance_an(hStart, vCurr, aCurr)

    dt = []
    h = []
    v = []  # na plusie, gdy spada
    a = []
    f = []

    while(t < tSimEnd):
        print("\n", t, ":\tt num:", time_to_distance_num )
        print(t, ":\tt an:", time_to_distance_an )
        print("\td:", hCurr)
        print("\tv:", vCurr)
        time_to_distance_num = time_to_reach_distance_num(hStart, vCurr, aCurr)
        time_to_distance_an = time_to_reach_distance_an(hStart, vCurr, aCurr)
        dt.append(t)

        a.append(aCurr)
        v.append(vCurr)
        h.append(hCurr)
        f.append(F(vCurr, hCurr) / Ms)

        aCurr = g #(F(vCurr, hCurr) / Ms)
        vCurr += aCurr * t_step
        hCurr -= vCurr * t_step

        t += t_step

        if hCurr <= 0 and vCurr > 5:
            print("crash")
            break
        else:
            if hCurr <= 0:
                print("Landed!")
                break


    plt.subplot(1, 3, 1)
    plt.plot(dt, h)
    plt.title("Wysokość")
    plt.xlabel("Czas [s]")
    plt.ylabel("Wysokość [m]")

    #
    plt.subplot(1, 3, 2)
    plt.plot(dt, v)
    plt.title("prędkość")
    plt.xlabel("Czas [s]")
    plt.ylabel("v")

    plt.subplot(1, 3, 3)
    plt.plot(dt, a)
    # plt.legend(["u_pi", "u"])
    plt.title("przyspieszenie")
    plt.xlabel("Czas [s]")
    plt.ylabel("a")
    plt.show()

    plt.subplot(1, 3, 1)
    plt.plot(dt, f)
    # plt.legend(["u_pi", "u"])
    plt.title("ciąg")
    plt.xlabel("Czas [s]")
    plt.ylabel("F")




