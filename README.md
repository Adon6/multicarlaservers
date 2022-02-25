# multicarlasevers
 
以下是 本项目研究计划和步骤
- 研究SUMO同步carla信息的原理
- 设计ZCM相关的消息结构 
- 实现使用 ZCM 同步两个服务器 智能体的状态消息
- 完善使用 ZCM 同步两台服务器 同步智能体及相关信息的消息同步
- 设计使用 ZCM 同步三台服务器的

## sumo 同步原理

2/25/2022
可以通过SUMO的源文件得到，SUMO将其自带的路网信息及车流信息通过carla_simulation.py， sumo_simulation.py, bridge_helper.py文件进行了合理的分解。其中carla_simulation.py文件将sumo系统中的车流信息导入至Carla中，对智能体相关的函数仅仅涉及了actor下的set_transform函数，即，仅仅涉及了智能体的location和rotation的参数。同时也更新了灯光等相关信息，在这里我们先忽略这部分内容。
在更新完carla内部的车路信息后，sumo plugin又将进行将进行下一步的动作，即，更新车流的route。更新完route后，sumo plugin将车路信息更新至sumo。在这过程中，sumo和carla内部的信息转换会涉及一些参考系的变换等工作，这些工作就交给了brigde_helper.py

以下是carla_simulation.py的函数

```
    def synchronize_vehicle(self, vehicle_id, transform, lights=None):
        """
        Updates vehicle state.

            :param vehicle_id: id of the actor to be updated.
            :param transform: new vehicle transform (i.e., position and rotation).
            :param lights: new vehicle light state.
            :return: True if successfully updated. Otherwise, False.
        """
        vehicle = self.world.get_actor(vehicle_id)
        if vehicle is None:
            return False

        vehicle.set_transform(transform)
        if lights is not None:
            vehicle.set_light_state(carla.VehicleLightState(lights))
        return True
```
其中vehicle.set_transform即改变从车辆状态的函数

参考以上原理，我们可以大体涉及出两台服务器中，carla的信息同步问题。
首先是智能体消息结构的设计。我们仅仅需要设计Transform消息体即可（包含location及rotation）
其次的服务器之间的互联，因为都是carla服务器，不存在参考系转换等问题。我们可以在同步两台服务器后，选择让两台服务器异步的传送车流信息。

##