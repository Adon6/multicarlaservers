
# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================

import argparse
import logging
import time

# ==================================================================================================
# -- find carla module -----------------------------------------------------------------------------
# ==================================================================================================

import glob
import os
import sys

try:
    sys.path.append(
        glob.glob('../PythonAPI/carla/dist/carla-*%d.%d-%s.egg' %
                  (sys.version_info.major, sys.version_info.minor,
                   'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla  # pylint: disable=import-error

# ==================================================================================================
# -- find carla simulation module -----------------------------------------------------------------------------
# ==================================================================================================

from carlaSimulation import CarlaSimulation


class SimulationSynchronization(object):

    def __init__(self,
                 carla_simulation,
                 sync_vehicle_color=False,
                 sync_vehicle_lights=False):

        self.carla = carla_simulation
        self.sync_vehicle_color = sync_vehicle_color
        self.sync_vehicle_lights = sync_vehicle_lights

        # id list 
        self.actor_ids = {} # contains all the ids controlled in carla

        # BridgeHelper.blueprint_library = self.carla.world.get_blueprint_library()

        # Configuring carla simulation in sync mode.
        settings = self.carla.world.get_settings()
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = self.carla.step_length
        self.carla.world.apply_settings(settings)

        traffic_manager = self.carla.client.get_trafficmanager()
        traffic_manager.set_synchronous_mode(True)
        
        # servers
        self.servers = {}

    def get_carla_lights_state(self, current_carla_lights):
        """
        Returns carla vehicle light state based on sumo signals.
        """
        current_lights = current_carla_lights
        pass
        # will be changed later for updating the light state 
        """
        
        # Blinker right / emergency.
        if (any([
                bool(SumoVehSignal.BLINKER_RIGHT),
                bool( SumoVehSignal.BLINKER_EMERGENCY)
        ]) != bool(current_lights & carla.VehicleLightState.RightBlinker)):
            current_lights ^= carla.VehicleLightState.RightBlinker

        # Blinker left / emergency.
        if (any([
                bool( SumoVehSignal.BLINKER_LEFT),
                bool( SumoVehSignal.BLINKER_EMERGENCY)
        ]) != bool(current_lights & carla.VehicleLightState.LeftBlinker)):
            current_lights ^= carla.VehicleLightState.LeftBlinker

        # Break.
        if (bool( SumoVehSignal.BRAKELIGHT) !=
                bool(current_lights & carla.VehicleLightState.Brake)):
            current_lights ^= carla.VehicleLightState.Brake

        # Front (low beam).
        if (bool( SumoVehSignal.FRONTLIGHT) !=
                bool(current_lights & carla.VehicleLightState.LowBeam)):
            current_lights ^= carla.VehicleLightState.LowBeam

        # Fog.
        if (bool( SumoVehSignal.FOGLIGHT) !=
                bool(current_lights & carla.VehicleLightState.Fog)):
            current_lights ^= carla.VehicleLightState.Fog

        # High beam.
        if (bool( SumoVehSignal.HIGHBEAM) !=
                bool(current_lights & carla.VehicleLightState.HighBeam)):
            current_lights ^= carla.VehicleLightState.HighBeam

        # Backdrive (reverse).
        if (bool( SumoVehSignal.BACKDRIVE) !=
                bool(current_lights & carla.VehicleLightState.Reverse)):
            current_lights ^= carla.VehicleLightState.Reverse

        # Door open left/right.
        if (any([
                bool( SumoVehSignal.DOOR_OPEN_LEFT),
                bool( SumoVehSignal.DOOR_OPEN_RIGHT)
        ]) != bool(current_lights & carla.VehicleLightState.Position)):
            current_lights ^= carla.VehicleLightState.Position

        return current_lights
        """

    def tick(self):
        """
        Tick to simulation synchronization
        """
        # ---------------
        # sync
        # ---------------
        
        # get all carla actors list 
        self.carla.tick()

        carla_spawned_actors = self.carla.spawned_actors #- set(self.sumo2carla_ids.values())

        for carla_actor_id in carla_spawned_actors:
            carla_actor = self.carla.get_actor(carla_actor_id)

            carla_transform_old = carla_actor.get_transform()
            old_location = carla_transform_old.location
            old_rotation = carla_transform_old.rotation


            carla_transform = carla.Transform(
            carla.Location(old_location.x+5, old_location.y+5, old_location.z),
            old_rotation)
            print(f"the actors {carla_actor_id} are changed with location({old_location.x},{old_location.y},{old_location.z})")
            print(f"the actors {carla_actor_id} are changed with rotation({old_rotation.pitch},{old_rotation.yaw},{old_rotation.roll})")

            logging.info('transform transfer')

            if self.sync_vehicle_lights:
                carla_lights = self.get_carla_lights_state(carla_actor.get_light_state())
            else:
                carla_lights = None
                
            self.carla.synchronize_vehicle(carla_actor_id, carla_transform, carla_lights)


    def close(self):
        """
        Cleans synchronization.
        """
        # Configuring carla simulation in async mode.
        settings = self.carla.world.get_settings()
        settings.synchronous_mode = False
        settings.fixed_delta_seconds = None
        self.carla.world.apply_settings(settings)

        # Closing sumo and carla client.
        self.carla.close()


def synchronization_loop(args):
    """
    Entry point for sumo-carla co-simulation.
    """

    carla_simulation = CarlaSimulation(args.carla_host, args.carla_port, args.step_length)

    synchronization = SimulationSynchronization(carla_simulation, args.sync_vehicle_color, args.sync_vehicle_lights)
    try:
        while True:
            start = time.time()

            synchronization.tick()

            end = time.time()
            elapsed = end - start
            if elapsed < args.step_length:
                time.sleep(args.step_length - elapsed)
            logging.info('ticked.')

    except KeyboardInterrupt:
        logging.info('Cancelled by user.')

    finally:
        logging.info('Cleaning synchronization')

        synchronization.close()


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument('--carla-host',
                           metavar='H',
                           default='127.0.0.1',
                           help='IP of the carla host server (default: 127.0.0.1)')
    argparser.add_argument('--carla-port',
                           metavar='P',
                           default=2000,
                           type=int,
                           help='TCP port to listen to (default: 2000)')
    argparser.add_argument('--master-host',
                           metavar='M',
                           default='127.0.0.1',
                           help='IP of the carla host server (default: 127.0.0.1)')
    argparser.add_argument('--master-port',
                           metavar='Q',
                           default=2000,
                           type=int,
                           help='TCP port to listen to (default: 2000)')
    argparser.add_argument('--slave-host',
                           metavar='S',
                           default='127.0.0.1',
                           help='IP of the carla host server (default: 127.0.0.1)')
    argparser.add_argument('--slave-port',
                           metavar='R',
                           default=2000,
                           type=int,
                           help='TCP port to listen to (default: 2000)')

    argparser.add_argument('--step-length',
                           default=0.05,
                           type=float,
                           help='set fixed delta seconds (default: 0.05s)')
    argparser.add_argument('--client-order',
                           metavar='TRACI_CLIENT_ORDER',
                           default=1,
                           type=int,
                           help='client order number for the co-simulation TraCI connection (default: 1)')
    argparser.add_argument('--sync-vehicle-lights',
                           action='store_true',
                           help='synchronize vehicle lights state (default: False)')
    argparser.add_argument('--sync-vehicle-color',
                           action='store_true',
                           help='synchronize vehicle color (default: False)')
    argparser.add_argument('--sync-vehicle-all',
                           action='store_true',
                           help='synchronize all vehicle properties (default: False)')
    argparser.add_argument('--debug', action='store_true', help='enable debug messages')
    arguments = argparser.parse_args()

    if arguments.sync_vehicle_all is True:
        arguments.sync_vehicle_lights = True
        arguments.sync_vehicle_color = True

    if arguments.debug:
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

    synchronization_loop(arguments)
