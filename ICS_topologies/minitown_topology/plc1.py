from basePLC import BasePLC
from utils import PLC1_DATA, STATE, PLC1_PROTOCOL
from utils import TANK, PLC1_ADDR, CONTROL
from datetime import datetime
from decimal import Decimal
import threading
import sys


class PLC1(BasePLC):

    def pre_loop(self):
        print 'DEBUG: plc1 enters pre_loop'
        self.local_time = 0
        self.reader = True
        self.tank_level = Decimal(self.get(TANK))
        self.saved_tank_levels = [["iteration", "timestamp", "TANK_LEVEL"]]
        path = 'plc1_saved_tank_levels_received.csv'        self.lock = threading.Lock()
        lastPLC = True
        week_index = int(sys.argv[1])
        BasePLC.set_parameters(self, path, self.saved_tank_levels, [TANK], [self.tank_level],
                               self.reader, self.lock, PLC1_ADDR, lastPLC, week_index)
        self.startup()

    def main_loop(self):
        """plc1 main loop.
            - reads sensors value
            - drives actuators according to the control strategy
            - updates its enip server
        """
        fake_values = []
        while True:
            control = int(self.get(CONTROL))
            if control == 0:
                self.local_time += 1
                tank_level = Decimal(self.get(TANK))
                #self.saved_tank_levels.append([datetime.now(), tank_level])
if __name__ == "__main__":
    plc1 = PLC1(
        name='plc1',
        state=STATE,
        protocol=PLC1_PROTOCOL,
        memory=PLC1_DATA,
        disk=PLC1_DATA)


