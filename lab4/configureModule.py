# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================

import logging

# ==================================================================================================
# -- import yaml ------------------------------------------------------------------------------------
# ==================================================================================================

import sys, os

import yaml

# ==================================================================================================
# -- configure ---------------------------------------------------------------------------------
# ==================================================================================================

class ConfigureModule(object):
    def __init__(self):
        ## 多服务器之间的进入/退出。需要服务器之间的确认，在双服务器的情况下先忽略
        self.servers_id = set()
        self.servers_IP = {}  # id:(host,port)
        self.subs = []

    def load_configure(self,path = "carlaservers.yaml"):
        with open(path,'r') as f:
            temp = yaml.load(f.read(), Loader=yaml.FullLoader)
            tempkeys = temp.keys()
            server_id = 0
            for s in temp['servers']:
                host = s['host']
                port = s['port']
                self.servers_IP[server_id] = (host,port)
                self.servers_id.add(server_id) 
                server_id += 1
                logging.info("Configure has been loaded, server: "+ host +":"+str(port) +" .")
            if 'actorcolor'in tempkeys and temp['actorcolor'] in (True,1,"True","true"):
                self.actorcolor = True
            else:
                self.actorcolor = False
            if 'actorlights' in tempkeys and temp['actorlights'] in (True,1,"True","true"):
                self.actorlights = True
            else:
                 self.actorlights = False
            if 'trafficlights' in tempkeys and temp['trafficlights'] in (True,1,"True","true"):
                self.trafficlights = True
            else:
                self.trafficlights = False
            if 'weather' in tempkeys and temp['weather'] in (True,1,"True","true"):
                self.weather = True
            else:
                self.weather = False
            if 'step_length' in tempkeys and temp['step_length'] < 0.01:
                self.step_length = 0.05
            else:
                self.step_length = temp['step_length'] 
            logging.info("Configure actor color sync: {} ".format(self.actorcolor))
            logging.info("Configure actor lights sync: {} ".format(self.actorlights))
            logging.info("Configure traffic lights sync: {} ".format(self.trafficlights))
            logging.info("Configure weather sync:{}".format(self.weather))
            logging.info("Configure step length is:{}".format(self.step_length))


    def get_servers_id(self):
        """
            返回一个集合
        """
        return self.servers_id

    def get_servers_IP(self):
        """
            返回服务器ip字典
        """
        return self.servers_IP