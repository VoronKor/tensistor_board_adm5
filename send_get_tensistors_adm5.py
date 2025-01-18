import serial
import time

port = '/dev/ttyS2'
baudrate = 9600

ser = serial.Serial(port, 9600)
HOST_REPORT_TIME = 0.2

class Temperature_HOST:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.reactor = self.printer.get_reactor()
        self.name = config.get_name().split()[-1]
        self.temp = self.min_temp = self.max_temp = 0.0

        self.printer.add_object("temperature_load " + self.name, self)

        if self.printer.get_start_args().get('debugoutput') is not None:
            return
        self.sample_timer = self.reactor.register_timer(
            self._sample_pi_temperature)

        self.printer.register_event_handler("klippy:connect",
                                            self.handle_connect)

    def handle_connect(self):
        self.reactor.update_timer(self.sample_timer, self.reactor.NOW)

    def setup_minmax(self, min_temp, max_temp):
        self.min_temp = min_temp
        self.max_temp = max_temp

    def setup_callback(self, cb):
        self._callback = cb

    def get_report_time_delta(self):
        return HOST_REPORT_TIME

    def _sample_pi_temperature(self, eventtime):
        try:
            ser.write('H7 \0\0\0\0\0\0\0'.encode())
            time.sleep(0.05)
            message = ser.readline().decode('utf-8').rstrip().split()
            ntemp = message[4]
            self.temp = float(ntemp)
        except Exception:
            logging.exception("temperature_load: Error reading data")
            self.temp = 0.0
            return self.reactor.NEVER

        if self.temp < self.min_temp:
            self.temp = self.min_temp

        if self.temp > self.max_temp:
            self.temp = self.max_temp

        mcu = self.printer.lookup_object('mcu')
        measured_time = self.reactor.monotonic()
        self._callback(mcu.estimated_print_time(measured_time), self.temp)
        return measured_time + HOST_REPORT_TIME

    def get_status(self, eventtime):
        return {
            'temperature': round(self.temp, 2),
        }

class tesistorsUart:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.reactor = self.printer.get_reactor()
        self.gcode = self.printer.lookup_object('gcode')

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
    # Register sensor
    pheaters = config.get_printer().load_object(config, "heaters")
    pheaters.add_sensor_factory("temperature_load", Temperature_HOST)

    return tesistorsUart(config)
