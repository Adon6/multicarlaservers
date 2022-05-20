import logging

# ==================================================================================================
# -- find zcm-structure module ---------------------------------------------------------------------
# ==================================================================================================
import sys, os

blddir= os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, blddir+"/zcm")
print(blddir)

from location_t import location_t
from rotation_t import rotation_t
from transformation_t import transformation_t
from transformation_group import transformation_group



# ==================================================================================================
# -- carla simulation ------------------------------------------------------------------------------
# ==================================================================================================


class CarlaSimulation(object):
    """
    CarlaSimulation is responsible for the management of the carla simulation.
    """
    def __init__(self, host=0, port=0, step_length=0):
        '''
        self.client = carla.Client(host, port)
        self.client.set_timeout(2.0)

        self.world = self.client.get_world()
        self.blueprint_library = self.world.get_blueprint_library()
        self.step_length = step_length

        # The following sets contain updated information for the current frame.
        self._active_actors = set()
        self.spawned_actors = set()
        self.destroyed_actors = set()

        # Set traffic lights.
        self._tls = {}  # {landmark_id: traffic_ligth_actor}

        tmp_map = self.world.get_map()
        for landmark in tmp_map.get_all_landmarks_of_type('1000001'):
            if landmark.id != '':
                traffic_ligth = self.world.get_traffic_light(landmark)
                if traffic_ligth is not None:
                    self._tls[landmark.id] = traffic_ligth
                else:
                    logging.warning('Landmark %s is not linked to any traffic light', landmark.id)

        ''' 
        # for simulation of lab 2
        self.actors = {} # id : actor
    class location:
        def __init__(self,x,y,z):
            self.x =x
            self.y =y
            self.z =z

    class rotation:
        def __init__(self,pitch,yaw,roll):
            self.pitch = pitch
            self.yaw = yaw
            self.roll = roll

    class transform:
        def __init__(self,location,rotation):
            self.location = location
            self.rotation = rotation
    class actor(object):
        def __init__(self,transform):
            self.id = id
            self.transformation = transform

        def get_transform(self):
            return self.transformation

        def set_transform(self,transform):
            self.transformation = transform

    def set_testdata(self):
        testdata = [ 
            (1,1,1,10,10,10),
            (2,2,2,9,9,9),
            (3,3,3,8,8,8),
            (4,4,4,7,7,7),
            (5,5,5,6,6,6)
            ]
        transformlist = []
        for i in testdata:
            alo = self.location(i[0],i[1],i[2])
            aro = self.rotation(i[3],i[4],i[5])
            atra = self.transform(alo,aro) 
            acto = self.actor(atra)
            transformlist.append(acto)
        for i in range(5):
            self.actors[i] = transformlist[i]
        logging.info("testdata has been set successfully!")

    def get_transforms(self):
        transform_list = []
        carla_actors = self.get_actors()
        for carla_actor_id in carla_actors:
            carla_actor = self.get_actor(carla_actor_id)
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
        

    def get_actor(self, actor_id):
        """
        Accessor for carla actor.
        """
        return self.actors[actor_id]

    def get_actors(self,actor_ids=None):
        """
        Accessor for carla actors.
        """

        if actor_ids is None:
            return list(self.actors.keys())
        else:
            actorList = []
            for id in actor_ids:
                actorList.append(self.actors[id])
            return actorList
