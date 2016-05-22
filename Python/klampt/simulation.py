from robotsim import *
import simlog

class SimpleSimulator (Simulator):
    """A convenience class that enables logging and easy definition of simulation hooks.
    """
    def __init__(self,world):
        """Arguments:
        - world: a RobotWorld instance.
        """
        Simulator.__init__(self,world)
        #these are functions automatically called at each time step
        self.robotControllers = {}
        self.hooks = []
        self.hook_args = []

        #turn this on to save log to disk
        self.logging = False
        self.logger = None
        self.log_state_fn="simulation_state.csv"
        self.log_contact_fn="simulation_contact.csv"

    def beginLogging(self):
        self.logging = True
        self.logger = simlog.SimLogger(self.sim,self.log_state_fn,self.log_contact_fn)
    def endLogging(self):
        self.logging = False
        self.logger = None
    def pauseLogging(self,paused=True):
        self.logging=not paused
    def toggleLogging(self):
        if self.logging:
            self.pauseLogging()
        else:
            if self.logger==None:
                self.beginLogging()
            else:
                self.pauseLogging(False)

    def setController(self,robot,function):
        if isinstance(robot,int):
            index = robot
        elif isinstance(robot,RobotModel):
            index = robot.index
        self.robotControllers += [None]*(self.self.world.numRobots()-len(self.robotControllers))
        self.robotControllers[index] = function

    def addHook(self,objects,function):
        """For the world object or objects 'objects', applies a hook that gets called every
        simulation loop.  The objects may be certain identifiers, WorldModel items or SimBodies. 
        - Accepted names are: 'time', or any items in the world
        - If they are individual bodies, the corresponding SimBody objects are passed to function. 
        - If they are RobotModel's, the corresponding SimRobotController objects are passed to function.
        - Otherwise they are passed directly to function.
        """
        if not hasattr(objects,'__iter__'):
            objects = [objects]
        args = []
        for o in objects:
            if isinstance(o,(RobotModelLink,RigidObjectModel,TerrainModel)):
                args.append(self.sim.body(o))
            elif isinstance(o,RobotModel):
                args.append(self.sim.controller(o))
            elif isinstance(o,str):
                if o == 'time':
                    args.append(o)
                elif self.world.robot(o).world >= 0:
                    args.append(self.world.robot(o))
                elif self.world.terrain(o).world >= 0:
                    args.append(self.world.terrain(o))
                elif self.world.rigidObject(o).world >= 0:
                    args.append(self.world.rigidObject(o))
                else:
                    raise ValueError("String value "+o+" is unknown")
            else:
                args.append(o)
        self.hooks.append(function)
        self.hook_args.append(args)

    def simulate(self,dt):
        #Handle logging
        if self.logger: self.logger.saveStep()

        #Advance simulation
        for i,controller in self.robotControllers.iteritems():
            controller(self.sim.controller(i))
        for (hook,args) in zip(self.hooks,self.hook_args):
            resolvedArgs = []
            for a in args:
                if isinstance(a,str):
                    if a=='time':
                        resolvedArgs.append(sim.getTime())
                    else:
                        raise ValueError("Invalid unresolved argument",a)
            hook(*args)
        Simulator.simulate(self,dt)
        