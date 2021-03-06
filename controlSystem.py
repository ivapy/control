from util import Timer
import numpy as np

class controlSystem(object):

    def __init__(self, ceom, trajGenerator, trackBuilder, config=None):

        self.ceom = ceom
        self.trajGen = trajGenerator

        self.trackBuilder = trackBuilder
        self.trackSim = None
        self.simOut = []

        if config is not None:
            self.config = config

        self.iflag = False

    def setInitialState(self, istate):
        #TODO: Ensure that this always works
        state_size = self.trajGen.system.B.shape[0]
        if state_size == 2*istate.x.size:
            istate.x = np.pad(istate.x.flatten(), (0, istate.x.size), mode='constant').reshape((state_size, 1))

        self.istate = istate
        self.iflag = True

    def goto(self, fstate, duration=None):

        if not self.iflag:
            print("Error, no initial state")

        if len(self.simOut) == 0:
            tshift = 0
        else:
            tshift = self.simOut[-1].t[-1]

        if duration is not None:
            tspan = [0, duration]
            theTraj = self.trajGen.point2point(self.istate.x, fstate, tspan)
        else:
            theTraj = self.trajGen.point2point(self.istate.x, fstate)

        if self.trackSim is None:
            self.trackSim = self.trackBuilder.firstBuildFromStruct(self.istate, theTraj)
        else:
            self.trackBuilder.reconfigFromStruct(self.trackSim, self.istate, theTraj)

        simsol = self.trackSim.simulate()

        simsol.traj = theTraj
        simsol.istate = self.istate
        simsol.fstate = self.trackSim.getState()

        self.addSim(simsol)
        self.iflag = False

        return simsol


    '''=============================== follow ==============================
    %
    % @brief  Specify that the system should follow the specified
    %         trajectory.
    %
    % @param[in]  desTraj Desired trajectory structure. 
    %
    % @param[out] simsol  Solution to the current simulated time span.
    %'''

    def follow(self, desTraj):

        if (not self.iflag):
            print('Error! Defined a terminal system state, but there is no initial state.')

        theTraj = self.trajGen.followPath(self.istate, desTraj)

        if self.trackSim is None:
            self.trackSim = self.trackBuilder.firstBuildFromStruct(self.istate, theTraj)
        else:
            self.trackBuilder.reconfigFromStruct(self.trackSim, self.istate, theTraj)

        with Timer(name="Sim"):
            simsol = self.trackSim.simulate()

        simsol.traj = theTraj
        simsol.istate = self.istate
        simsol.fstate = self.trackSim.getState()

        self.addSim(simsol)
        self.iflag = False

        return simsol

    # WIP to track trajectories without using feed forward
    # TODO: Test
    def track(self, desTraj):
        if (not self.iflag):
            print('Error! Defined a terminal system state, but there is no initial state.')

        if self.trackSim is None:
            self.trackSim = self.trackBuilder.firstBuildFromStruct(self.istate, desTraj)
        else:
            self.trackBuilder.reconfigFromStruct(self.trackSim, self.istate, desTraj)

        with Timer(name="Sim"):
            simsol = self.trackSim.simulate()

        simsol.traj = desTraj
        simsol.istate = self.istate
        simsol.fstate = self.trackSim.getState()

        self.addSim(simsol)
        self.iflag = False

        return simsol



    def addSim(self, simOut):
        #if len(self.simOut) == 0:
        self.simOut.append(simOut)