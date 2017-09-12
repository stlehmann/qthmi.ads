from qthmi.main.connector import AbstractPLCConnector, ConnectionError
import pyads


__author__ = 'Stefan Lehmann'


class ADSConnector(AbstractPLCConnector):
    """
    Basic Connector class for connecting to the ADS device.

    :ivar int port: port number to the ADS device
    :ivar ams_addr: ip adress of the ADS device

    The ``ams_addr`` is set to the address of the local host and
    the port is set to PORT_SPS1 (801).

    """

    def __init__(self, ams_addr=None, port=None):
        super(ADSConnector, self).__init__()
        self.port = pyads.open_port()
        self.ams_addr = ams_addr or pyads.get_local_address()
        self.ams_addr.port = port or pyads.PORT_SPS1

    def read_from_plc(self, address, datatype):
        """
        Read value from the plc.

        :param int address: memory address
        :param datatype: ``c`` datatype, a PLCTYPE constant

        The PLCTYPE constants are found in the :py:mod:`qthmi.ads.constants`
        module.

        """
        index_group = (pyads.INDEXGROUP_MEMORYBIT
                       if datatype == pyads.PLCTYPE_BOOL
                       else pyads.INDEXGROUP_MEMORYBYTE)

        (errcode, value) = pyads.read(self.ams_addr, index_group,
                                      address, datatype)

        if errcode:
            raise ConnectionError(
                "Reading from address %i (ErrorCode %i)" %
                (address, errcode)
            )
        return value

    def write_to_plc(self, address, value, datatype):
        """
        Write value to the plc.

        :param int address: memory address
        :param value: value to be written
        :param datatype: ``c`` datatype, a PLCTYPE constant

        The PLCTYPE constants are found in the :py:mod:`qthmi.ads.constants`
        module.

        """
        index_group = (pyads.INDEXGROUP_MEMORYBIT
                       if datatype == pyads.PLCTYPE_BOOL
                       else pyads.INDEXGROUP_MEMORYBYTE)

        errcode = pyads.write(self.ams_addr, index_group, address,
                              value, datatype)

        if errcode:
            raise ConnectionError(
                "Writing on address %i (ErrorCode %i)" %
                (address, errcode)
            )
