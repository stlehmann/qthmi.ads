__author__ = 'Stefan Lehmann'

from qthmi.main.connector import AbstractPLCConnector, ConnectionError
from pyads import adsPortOpen, adsGetLocalAddress, adsSyncReadReq, adsSyncWriteReq
from constants import *


class ADSConnector(AbstractPLCConnector):
    """
    Basic Connector class for connecting to the ADS device.
    
    :ivar int port: port number to the ADS device
    :ivar ams_addr: ip adress of the ADS device
    
    The ``ams_addr`` is set to the address of the local host and
    the port is set to PORT_SPS1 (801).

    """

    def __init__(self):
        super(ADSConnector, self).__init__()
        self.port = adsPortOpen()
        self.ams_addr = adsGetLocalAddress()

        if self.ams_addr.errCode:
            raise ADSError(self.adsAdr.errCode())

        self.ams_addr.setPort(PORT_SPS1)

    def read_from_plc(self, address, datatype):
        """
        Read value from the plc.
        
        :param int address: memory address
        :param datatype: ``c`` datatype, a PLCTYPE constant
        
        The PLCTYPE constants are found in the :py:mod:`qthmi.ads.constants` module.
        
        """
        index_group = INDEXGROUP_MEMORYBIT if datatype == PLCTYPE_BOOL else INDEXGROUP_MEMORYBYTE
        (errcode, value) = adsSyncReadReq(self.ams_addr, index_group, address, datatype)
        if errcode:
            raise ConnectionError("Reading from address %i (ErrorCode %i)" % (address, errcode))
        return value

    def write_to_plc(self, address, value, datatype):
        """
        Write value to the plc.
        
        :param int address: memory address
        :param value: value to be written
        :param datatype: ``c`` datatype, a PLCTYPE constant
        
        The PLCTYPE constants are found in the :py:mod:`qthmi.ads.constants` module.
        
        """
        index_group = INDEXGROUP_MEMORYBIT if datatype == PLCTYPE_BOOL else INDEXGROUP_MEMORYBYTE
        errcode = adsSyncWriteReq(self.ams_addr, index_group, address, value, datatype)
        if errcode:
            raise ConnectionError("Writing on address %i (ErrorCode %i)" % (address, errcode))

