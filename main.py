import matplotlib.pyplot as plt


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def F(h, v):
    k1 = 1 * Ms + 0
    k2 = 1 * 1/g + 0
    result = k1 * v + k2 * h * -1 * pow(v, 2) / (2 * h)
    print("k1: ", k1 * v)
    print("k2: ",  k2 * h * -1 * pow(v, 2) / (2 * h) )

    print(result)
    if result < 0:
        return 0
    else:
        if result > Fmax:
            return result
        else:
            return result


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    G = 6.67 * pow(10, -11)  # stała grawitacyjna

    timestamp = 5  # czas miedzy pomiarami
    tSimEnd = 60
    hStart = 10000  # wysokosc poczatkowa
    vStart = 0  # predkosc m/s poczatkowa, dodatnia gdy zbliza się

    Ms = 500  # masa łazika
    Mp = 6.41 * pow(10, 23)  # masa planety
    Rp = 3389000  # m promien
    g = G * Mp / (Rp * Rp)  # grawitacja planety

    hCurr = hStart
    vCurr = vStart
    aCurr = g

    Fmax = 400  # N maksymalna przepustnica
    Fcurr = 0  # obecna przepustnica

    dt = []
    h = []
    v = []  # na plusie, gdy spada
    a = []
    f = []

    for i in range(0, 120):
        dt.append(i)

        a.append(aCurr)
        v.append(vCurr)
        h.append(hCurr)
        f.append(F(hCurr, vCurr) / Ms)

        aCurr -= F(hCurr, vCurr) / Ms
        vCurr += aCurr
        hCurr -= vCurr

        print("t:", i)

        print("a: ", a[i])
        print("v: ", v[i])
        print("h: ", h[i])

        if hCurr <= 0 and vCurr > 10:
            print("crash")
            break
        else:
            if hCurr <= 0 and vCurr < 10:
                print("Landed!")
                break

    plt.subplot(1, 4, 1)
    plt.plot(dt, h)
    plt.title("Wysokość łazika nad planetą")
    plt.xlabel("Czas [s]")
    plt.ylabel("Wysokość [m]")

    #
    plt.subplot(1, 4, 2)
    plt.plot(dt, v)
    plt.title("prędkość")
    plt.xlabel("Czas [s]")
    plt.ylabel("v")

    plt.subplot(1, 4, 3)
    plt.plot(dt, a)
    # plt.legend(["u_pi", "u"])
    plt.title("przyspieszenie")
    plt.xlabel("Czas [s]")
    plt.ylabel("a")

    plt.subplot(1, 4, 4)
    plt.plot(dt, f)
    # plt.legend(["u_pi", "u"])
    plt.title("ciąg")
    plt.xlabel("Czas [s]")
    plt.ylabel("F")
    plt.suptitle("przysp")

    plt.show()
