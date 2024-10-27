import serial
import time

port = '/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0'  
baudrate = 9600

ser = serial.Serial(port, 9600)

class tesistorsUart:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.reactor = self.printer.get_reactor()
        self.gcode = self.printer.lookup_object('gcode')
        #port = config.get('path')
        self.message = config.get('message', 'Welcome to Klipper!')
        ser.write('H7 \0\0\0\0\0\0\0'.encode())
        self.gcode.register_command(
            'H7', self.cmd_H7, desc=self.cmd_H7_help)
        self.gcode.register_command(
            'H1', self.cmd_H1, desc=self.cmd_H1_help)
        self.gcode.register_command(
            'H2', self.cmd_H2, desc=self.cmd_H2_help)
        self.gcode.register_command(
            'H3', self.cmd_H3, desc=self.cmd_H3_help)

        self.printer.register_event_handler(
            'klippy:ready', self._ready_handler)

    def _ready_handler(self):
        waketime = self.reactor.monotonic() + 1
        self.reactor.register_timer(self._H7, waketime)

    def _H7(self, eventtime=None):
        ser.write('H7 \0\0\0\0\0\0\0'.encode())
        time.sleep(0.05)
        self.message=ser.readline().decode('utf-8').rstrip()
        self.gcode.respond_info(self.message)
        return self.reactor.NEVER
    cmd_H7_help = "H7"
    def cmd_H7(self, gcmd):
        self._H7()

    def _H1(self, eventtime=None):
        ser.write('H1 \0\0\0\0\0\0\0'.encode())
        time.sleep(0.05)
        self.message=ser.readline().decode('utf-8').rstrip()
        self.gcode.respond_info(self.message)
        return self.reactor.NEVER
    cmd_H1_help = "Greet the user"
    def cmd_H1(self, gcmd):
        self._H1()
    def _H2(self, eventtime=None):
        ser.write('H2 S500 \0\0'.encode())
        time.sleep(0.05)
        self.message=ser.readline().decode('utf-8').rstrip()
        self.gcode.respond_info(self.message)
        return self.reactor.NEVER
    cmd_H2_help = "H2"
    def cmd_H2(self, gcmd):
        self._H2()

    def _H3(self, eventtime=None):
        ser.write('H3 S200 \0\0'.encode())
        time.sleep(0.05)
        self.message=ser.readline().decode('utf-8').rstrip()
        self.gcode.respond_info(self.message)
        return self.reactor.NEVER
    cmd_H3_help = "H3"
    def cmd_H3(self, gcmd):
        self._H3()        
    	
def load_config(config):
    return tesistorsUart(config)