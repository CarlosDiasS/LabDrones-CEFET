from pymavlink import mavutil
import time

CONNECTION_STRING = "udp:127.0.0.1:14550"
#CONNECTION_STRING = "/dev/ttyS0" 

ALTITUDE = 10

def connect():
    print(f"Conectando em {CONNECTION_STRING}...")
    drone = mavutil.mavlink_connection(CONNECTION_STRING, baud=57600)
    print("Aguardando heartbeat...")
    drone.wait_heartbeat()
    print(f"Heartbeat recebido (sys={drone.target_system}, comp={drone.target_component})")
    return drone

def set_mode(drone, mode_name):

    mode_id = drone.mode_mapping()[mode_name]

    print(f"Alterando para {mode_name} ({mode_id})")

    drone.set_mode(mode_id)

    # espera confirmação
    while True:
        hb = drone.recv_match(type="HEARTBEAT", blocking=True, timeout=2)
        if not hb:
            continue

        print(f"Modo atual: {hb.custom_mode}")

        if hb.custom_mode == mode_id:
            print("Modo confirmado")
            return

def arm(drone):

    print("Armando motores...")

    drone.arducopter_arm()
    drone.motors_armed_wait()

    print("Motores armados")


def takeoff(drone, altitude):

    print(f"Decolando para {altitude} m")

    drone.mav.command_long_send(
        drone.target_system,
        drone.target_component,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
        0,
        0, 0, 0, 0,
        0, 0,
        altitude
    )
    while True:

        msg = drone.recv_match(
            type="GLOBAL_POSITION_INT",
            blocking=True
        )

        current_alt = msg.relative_alt / 1000.0

        print(f"Altitude: {current_alt:.1f} m")

        if current_alt >= altitude * 0.95:
            print("Altitude atingida")
            break

def rtl(drone):

    print("RTL")

    drone.mav.command_long_send(
        drone.target_system,
        drone.target_component,
        mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH,
        0,
        0, 0, 0, 0,
        0, 0, 0
    )

def wait(seconds):
    time.sleep(seconds)

def main():

    drone = connect()

    set_mode(drone, "GUIDED")

    arm(drone)

    takeoff(drone, ALTITUDE)

    wait(20)

    set_mode(drone, "RTL")

if __name__ == "__main__":
    main()