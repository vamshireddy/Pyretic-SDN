################################################################################
# The Pyretic Project                                                          #
# frenetic-lang.org/pyretic                                                    #
# author: Joshua Reich (jreich@cs.princeton.edu)                               #
# author: Nick Feamster (feamster@cc.gatech.edu)                               #
################################################################################

from pyretic.lib.corelib import *
from pyretic.lib.std import *

def learn(self):
    """Standard MAC-learning logic"""
    def update_policy():
        """Update the policy based on current forward and query policies"""
        self.policy = self.forward + self.query
    self.update_policy = update_policy

    def learn_new_MAC(pkt):
        """Update forward policy based on newly seen (mac,port)"""
        self.forward = if_(match(dstmac=pkt['srcmac'],
                                switch=pkt['switch']),
                          fwd(pkt['inport']),
                          self.forward) 
        self.update_policy()

    def set_initial_state():
        self.query = packets(1,['srcmac','switch'])
        self.query.register_callback(learn_new_MAC)
        self.forward = self.flood  # REUSE A SINGLE FLOOD INSTANCE
        self.update_policy()

    self.flood = flood()           # REUSE A SINGLE FLOOD INSTANCE
    set_initial_state()


def mac_learner():
    """Create a dynamic policy object from learn()"""
    return dynamic(learn)()

def main():
    return mac_learner()
