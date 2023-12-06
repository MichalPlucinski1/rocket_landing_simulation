import matplotlib.pyplot as plt

# Constants
mass = 1000  # Mass of the spaceship in kg
initial_speed = 10  # Initial speed in m/s
initial_distance = 6000  # Initial distance from Mars in meters
gravity = 9.81  # Acceleration due to gravity on Mars in m/s^2

# Lists to store data for plotting
time_list = []
distance_list = []
velocity_list = []
acceleration_list = []
thrust_list = []

# Function to calculate thrust based on distance and velocity
def F(distance, velocity):
    # Required to be thrust to land safely
    if distance <= 0:
        return 0  # If distance is 0 or negative, no thrust is needed (already landed)
    else:
        required_thrust = mass * (velocity ** 2) / (2 * distance)
        return required_thrust  # Limit thrust to maximum 1500 Newtons


if __name__ == '__main__':

    # Initial conditions
    time = 0
    distance = initial_distance
    velocity = initial_speed
    acceleration = 0

    # Simulation loop
    while distance > 0:
        print("t:",time,"d",distance,"v",velocity)
        time_list.append(time)
        distance_list.append(distance)
        velocity_list.append(velocity)
        acceleration_list.append(gravity)  # Acceleration due to gravity on Mars

        # Calculate required thrust using the F function
        thrust = F(distance, velocity)
        thrust_list.append(thrust)

        # Update time
        time += 1

        # Update acceleration and velocity
        acceleration = (thrust - gravity) / mass  # Thrust minus gravity, divided by mass
        velocity += acceleration
        distance -= velocity  # Update distance based on the new velocity

    # Plotting graphs
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 4, 1)
    plt.plot(time_list, distance_list)
    plt.title('Distance vs Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Distance (m)')
    plt.grid(True)

    plt.subplot(1, 4, 2)
    plt.plot(time_list, velocity_list)
    plt.title('Velocity vs Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity (m/s)')
    plt.grid(True)

    plt.subplot(1, 4, 3)
    plt.plot(time_list, acceleration_list)
    plt.title('Acceleration vs Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (m/s²)')
    plt.grid(True)

    plt.subplot(1, 4, 4)
    plt.plot(time_list, thrust_list)
    plt.title('Thrust vs Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Thrust (N)')
    plt.grid(True)

    plt.tight_layout()
    plt.show()