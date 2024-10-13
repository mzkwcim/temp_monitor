import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
from datetime import datetime

def get_cpu_temperature():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
            temp_str = file.read()
            temperature = float(temp_str) / 1000.0
            return temperature
    except FileNotFoundError:
        print("Nie można otworzyć pliku z temperaturą!")
        return None

def update_plot(frame, temps, times, line):
    temperature = get_cpu_temperature()
    if temperature is not None:
        times.append(datetime.now())  # Użycie obiektu datetime dla czasu
        temps.append(temperature)

        times = times[-60:]
        temps = temps[-60:]

        line.set_data(times, temps)

        ax.relim()
        ax.autoscale_view()

    return line,

def monitor_temperature():
    global ax

    temps = []
    times = []

    fig, ax = plt.subplots()
    ax.set_title("Temperatura CPU w czasie rzeczywistym")
    ax.set_xlabel("Czas")
    ax.set_ylabel("Temperatura (°C)")

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    locator = mdates.AutoDateLocator()  # Automatyczne dopasowanie znaczników osi X
    ax.xaxis.set_major_locator(locator)

    line, = ax.plot(times, temps, color='r')

    ani = animation.FuncAnimation(fig, update_plot, fargs=(temps, times, line), interval=1000, cache_frame_data=False)

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    plt.show()

if __name__ == "__main__":
    monitor_temperature()

