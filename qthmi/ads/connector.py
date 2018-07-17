"""Connector for ADS devices.

:author: Stefan Lehmann <stlm@posteo.de>
:license: MIT, see license file or https://opensource.org/licenses/MIT

:created on 2018-06-11 18:16:49
:last modified by: Stefan Lehmann
:last modified time: 2018-07-17 15:27:19

"""
from qthmi.main.connector import AbstractPLCConnector, ConnectionError
from .gui import VALUE_TYPE
import pyads


class ADSConnector(AbstractPLCConnector):
    """Basic Connector class for connecting to the ADS device.

    :ivar int port: port number to the ADS device
    :ivar ams_addr: ip adress of the ADS device

    The ``ams_addr`` is set to the address of the local host and
    the port is set to PORT_SPS1 (801).

    """

    def __init__(self, ams_addr: pyads.AmsAddr=None, port: int=None) -> None:
        super(ADSConnector, self).__init__()
        self.port = pyads.open_port()
        self.ams_addr = ams_addr or pyads.get_local_address()
        self.ams_addr.port = port or pyads.PORT_SPS1

    def read_from_plc(self, address: int, datatype: int) -> VALUE_TYPE:
        """Read value from the plc.

        :param int address: memory address
        :param datatype: ``c`` datatype, a PLCTYPE constant

        The PLCTYPE constants are found in the :py:mod:`qthmi.ads.constants`
        module.

        """
        index_group = (pyads.INDEXGROUP_MEMORYBIT
                       if datatype == pyads.PLCTYPE_BOOL
                       else pyads.INDEXGROUP_MEMORYBYTE)

        try:
            value = pyads.read(self.ams_addr, index_group, address, datatype)
        except pyads.ADSError as e:
            raise ConnectionError(
                "Reading from address %i (ErrorCode %i)" %
                (address, e.err_code)
            )
        return value

    def write_to_plc(self, address: int, value: VALUE_TYPE, datatype: int) -> None:
        """Write value to the plc.

        :param int address: memory address
        :param value: value to be written
        :param datatype: ``c`` datatype, a PLCTYPE constant

        The PLCTYPE constants are found in the :py:mod:`qthmi.ads.constants`
        module.

        """
        index_group = (pyads.INDEXGROUP_MEMORYBIT
                       if datatype == pyads.PLCTYPE_BOOL
                       else pyads.INDEXGROUP_MEMORYBYTE)

        try:
            pyads.write(self.ams_addr, index_group, address,
                        value, datatype)
        except pyads.ADSError as e:
            raise ConnectionError(
                "Writing on address %i (ErrorCode %i)" %
                (address, e.err_code)
            )
