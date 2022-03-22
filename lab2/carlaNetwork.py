# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================

import logging
import time

# ==================================================================================================
# -- import carla ----------------------------------------------------------------------------------
# ==================================================================================================

import carla  # pylint: disable=import-error

# ==================================================================================================
# -- import zcm ------------------------------------------------------------------------------------
# ==================================================================================================

from zerocm import ZCM
import sys, os

# ==================================================================================================
# -- find zcm-structure module ---------------------------------------------------------------------
# ==================================================================================================


blddir= os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, blddir+"/zcm")
print(blddir)

from location_t import location_t
from rotation_t import rotation_t
from transformation_t import transformation_t
from transformation_group import transformation_group


# ==================================================================================================
# -- find carlaSimulation module ---------------------------------------------------------------------
# ==================================================================================================

from carlaSimulation import CarlaSimulation

# ==================================================================================================
# -- carla network ---------------------------------------------------------------------------------
# ==================================================================================================

class carlaNetwork(object):
    def __init__(self, carla):
        # 首先要订阅zcm频道和发布zcm频道，所以我们需要知道网络内所有的用户,用户记录host,port即可
        ## 多服务器之间的进入/退出。需要服务器之间的确认，在双服务器的情况下先忽略
        self.servers_id = set()
        self.servers_ip = {}  # id:(host,port)
        ## 如果需要构成<环>或其他数据结构则再增加一个字典表示其相关的服务器
        self.servers_net = {} # id:(role,related)
        self.subs = []


    def add_server(self,server):
        pass

    def send_connect(self, url = "ipc"):
        self.zcm_sender = ZCM(url)
        if not self.zcm_sender.good():
            logging.info("Unable to initialize zcm sender with url: "+url)
            exit() ## 之后对其进行错误处理
        self.zcm_sender.start()

    def receive_connect(self, url="ipc"):
        self.zcm_receiver = ZCM(url)
        if not self.zcm_receiver.good():
            logging.info("Unable to initialize zcm receiver with url: "+url)
            exit() ## 之后对其进行错误处理
        self.zcm_receiver.start()


    def publish_transforms(self, transforms):
        self.zcm_sender.publish("Transforms", transforms)
        logging.info("Sucessfully published transforms")

    def subscribe_transforms(self, handler):
        sub = self.zcm_receiver.subscibe("Transforms",transformation_group, handler)
        self.subs.append(sub)
        logging.info("Sucessfully subscribed transforms")

    def unsubscribe(self):
        for sub in self.subs:
            self.zcm_receiver.unsubscribe(sub)

    def get_transforms(self, own_carla):
        transform_list = []
        carla_actors = own_carla.get_actors()
        for carla_actor_id in carla_actors:
            carla_actor = own_carla.get_actor(carla_actor_id)
            carla_actor_transform = carla_actor.get_transform()
            
            # generate zcm data strcture
            
            transformation = transformation_t()
            transformation.id = carla_actor_id
            transformation.location.x = carla_actor_transform.location.x
            transformation.location.y = carla_actor_transform.location.y
            transformation.location.z = carla_actor_transform.location.z
            transformation.rotation.pitch = carla_actor_transform.rotation.pitch
            transformation.rotation.yaw = carla_actor_transform.rotation.yaw
            transformation.rotation.roll = carla_actor_transform.rotation.roll
            transform_list.append(transformation)

        num_of_transform = len(transform_list)
        all_transforms = transformation_group()
        all_transforms.num_of_actor = num_of_transform
        all_transforms.transformation = transform_list.copy()
        return all_transforms
        
    def stop_channel(self):
        if self.zcm_receiver: 
            self.zcm_receiver.stop()
            logging.info("zcm_receiver has been stopped successfully")
        if self.zcm_sender: 
            self.zcm_sender.stop()
            logging.info("zcm_sender has been stopped successfully")

