# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================
import argparse
import logging
import time 

from zerocm import ZCM
import sys, os


from zcmNetwork import carlaNetwork
from carlaSimulation import CarlaSimulation

def synchronization_loop(args):
    """
    Entry point for sumo-carla co-simulation.
    """

    carla_simulation = CarlaSimulation(args.host, args.port, 0)
    send_url = "udpm://"+args.host + ":" + str(args.port) +"?ttl=256"
    logging.info(f'send_url is {send_url}')
    publisher = carlaNetwork(carla_simulation)
    publisher.send_connect(send_url)
    carla_simulation.set_testdata()

    transformation_list = carla_simulation.get_transforms()

    while(1):    
        publisher.publish_transforms("Transform",transformation_list)
        logging.info('transform sent!')
        time.sleep(1)
    
    publisher.stop_channel()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument('--host',
                           metavar='H',
                           default='127.0.0.1',
                           help='IP of the carla host server (default: 127.0.0.1)')
    argparser.add_argument('--port',
                           metavar='P',
                           default=2000,
                           type=int,
                           help='TCP port to listen to (default: 2000)')
    arguments = argparser.parse_args()

    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

    synchronization_loop(arguments)