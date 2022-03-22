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

def printout(channel,msg):
    logging.info(channel+" reveived.")
    print(msg)

def synchronization_loop(args):
    """
    Entry point for sumo-carla co-simulation.
    """

    carla_simulation = CarlaSimulation(args.host, args.port, 0)
    receive_url = "udpm://"+args.host + ":" + str(args.port) +"?ttl=256"
    logging.info(f'receive_url is {receive_url}')
    receiver = carlaNetwork(carla_simulation)
    receiver.receive_connect(receive_url)


    while(1):    
        receiver.subscribe_transforms("Transform",printout)
        logging.info('transforms received!')
        time.sleep(1)
    
    receiver.stop_channel()


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
    if arguments.debug:
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

    synchronization_loop(arguments)