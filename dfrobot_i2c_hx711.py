import time
import struct
from pinpong.board import gboard, I2C

# Define constants
I2C_ADDR = 0x64
REG_CLEAR_REG_STATE = 0x65
REG_DATA_GET_RAM_DATA = 0x66
REG_DATA_GET_CALIBRATION = 0x67
REG_DATA_GET_PEEL_FLAG = 0x69
REG_DATA_INIT_SENSOR = 0x70
REG_SET_CAL_THRESHOLD = 0x71
REG_SET_TRIGGER_WEIGHT = 0x72
REG_CLICK_RST = 0x73
REG_CLICK_CAL = 0x74

class DFRobot_HX711_I2C:
    def __init__(self, board=None, i2c_addr=I2C_ADDR, bus_num=0):
        if isinstance(board, int):
            i2c_addr = board
            board = gboard
        elif board is None:
            board = gboard
        self.i2c_addr = i2c_addr
        self._i2c = I2C(bus_num)
        self.buffer = bytearray(3)
        self.rxbuf = bytearray(16)
        self._offset = 0
        self._calibration = 1752.60

    def begin(self):
        time.sleep(0.03)
        self.buffer[0] = REG_DATA_INIT_SENSOR
        self._write_register()
        time.sleep(0.03)
        self.buffer[0] = REG_CLEAR_REG_STATE
        self._write_register()
        time.sleep(0.03)
        self._offset = self.average(1)
        self.setCalibration(self._calibration)

    def average(self, times=1):
        sum = 0
        for _ in range(times):
            sum += self.raw_weight()
        return sum / times

    def weight(self, times=1):
        weight = self.average(times)
        time.sleep(0.05)
        peel_flag = self.peelFlag()
        if peel_flag == 1:
            self._offset = self.average(times)
        elif peel_flag == 2:
            self._calibration = self.calibration()
        return (weight - self._offset) / self._calibration

    def raw_weight(self):
        self.buffer[0] = REG_DATA_GET_RAM_DATA
        self._write_register()
        time.sleep(0.03)
        self._read_register(4)
        return ((self.rxbuf[0] << 24) | (self.rxbuf[1] << 16) | (self.rxbuf[2] << 8) | self.rxbuf[3])

    def peel(self):
        self._offset = self.average(1)
        self.buffer[0] = REG_CLICK_RST
        self._write_register()
        time.sleep(0.03)

    def peelFlag(self):
        self.buffer[0] = REG_DATA_GET_PEEL_FLAG
        self._write_register()
        time.sleep(0.03)
        self._read_register(1)
        return self.rxbuf[0]

    def calibration(self):
        self.buffer[0] = REG_DATA_GET_CALIBRATION
        self._write_register()
        time.sleep(0.03)
        self._read_register(4)
        value = (self.rxbuf[0] << 24) | (self.rxbuf[1] << 16) | (self.rxbuf[2] << 8) | self.rxbuf[3]
        return struct.unpack('>f', struct.pack('>I', value))[0]

    def enableCalibration(self):
        self.buffer[0] = REG_CLICK_CAL
        self._write_register()
        time.sleep(0.03)

    def setCalibration(self, cal):
        self._calibration = cal

    def setCalThreshold(self, cal):
        self.buffer[0] = REG_SET_CAL_THRESHOLD
        tx_data = struct.pack('>H', cal)
        self.buffer[1:3] = tx_data
        self._write_register()
        time.sleep(0.03)

    def setTriggerWeight(self, weight):
        self.buffer[0] = REG_SET_TRIGGER_WEIGHT
        tx_data = struct.pack('>H', weight)
        self.buffer[1:3] = tx_data
        self._write_register()
        time.sleep(0.03)

    def _write_register(self):
        self._i2c.writeto(self.i2c_addr, self.buffer)

    def _read_register(self, length):
        self.rxbuf = self._i2c.readfrom(self.i2c_addr, length)
