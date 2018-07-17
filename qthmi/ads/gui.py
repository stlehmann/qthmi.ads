"""Mapper for the GUI.

:author: Stefan Lehmann <stlm@posteo.de>
:license: MIT, see license file or https://opensource.org/licenses/MIT

:created on 2018-06-11 18:16:49
:last modified by: Stefan Lehmann
:last modified time: 2018-07-17 14:17:09

"""
from typing import Union, List, Optional, Any
from pyads import (
    AmsAddr,
    adsSyncWriteReq,
    adsSyncReadReq,
    INDEXGROUP_MEMORYBIT,
    PLCTYPE_BOOL,
    INDEXGROUP_MEMORYBYTE,
)
from qthmi.main.widgets import HMIObject


VALUE_TYPE = Optional[Union[float, int]]


class ADSMapper:
    """Mapper for the ADS protocol.

    Objects of this class represent a plc process value. The class
    accomblishes a connection between plc and the gui. For implementing
    the interaction between gui objects and plc values subclass and implement
    mapAdsToGui according to the given examples.

    :param int plcAddress: plc address
    :param plcDataType: plc data type
    :param guiObjects: list/tuple or single gui objects
        (for instance Qt objects)
    :param string hint: hint for the plv value

    Sample code::

    >>> class TextBoxMapper (ADSMapper):
    >>>     def mapAdsToGui(self, guiObject, value):
    >>>         guiObject.setText(str(value))

    >>> class ComboBoxMapper (ADSMapper):
    >>>     def mapAdsToGui(self, guiObject, value):
    >>>         index = guiObject.findData(QVariant(value))
    >>>         guiObject.setCurrentIndex(index)

    >>> class DSpinBoxMapper (ADSMapper):
    >>>     def mapAdsToGui(self, guiObject, value):
    >>>         guiObject.setValue(float(value))

    >>> class SpinBoxMapper (ADSMapper):
    >>>     def mapAdsToGui(self, guiObject, value):
    >>>         guiObject.setValue(int(value))

    >>> class BinaryMapper (ADSMapper):
    >>>     def mapAdsToGui(self, guiObject, value):
    >>>         guiObject.setText(__builtin__.bin(int(value)))

    """

    def __init__(
        self,
        plcAddress: int,
        plcDataType: int,
        guiObjects: List[HMIObject],
        hint: str = None,
    ) -> None:
        self.hint = hint
        self.plcAdr = plcAddress
        self.plcDataType = plcDataType
        self.currentValue: VALUE_TYPE = None
        self.guiObjects = guiObjects

        if isinstance(guiObjects, (list, tuple)):
            for o in guiObjects:
                o.plcObject = self
        else:
            guiObjects.plcObject = self

    def write(self, adsAdr: int, value: VALUE_TYPE) -> None:
        """Write a value to the plc address.

        :param qthmi.ads.constants.AmsAdr adsAdr: address to the ADS device
        :param value: value to be written

        """
        self.currentValue = value
        indexgroup = (
            INDEXGROUP_MEMORYBIT
            if self.plcDataType == PLCTYPE_BOOL
            else INDEXGROUP_MEMORYBYTE
        )
        err = adsSyncWriteReq(
            adsAdr, indexgroup, self.plcAdr, self.currentValue, self.plcDataType
        )
        if err == 0:
            return
        raise Exception(
            "error writing on address %i. error number %i" % (self.plcAdr, err)
        )

    def read(self, adsAdr: AmsAddr) -> Any:
        """Read from plc address and write in self.currentValue.

        Call mapAdsToGui to show the value on the connected gui objects.

        :param qthmi.ads.constants.AmsAdr adsAdr: address to the ADS
            device
        :return: current value

        """
        indexgroup = (
            INDEXGROUP_MEMORYBIT
            if self.plcDataType == PLCTYPE_BOOL
            else INDEXGROUP_MEMORYBYTE
        )
        (err, value) = adsSyncReadReq(adsAdr, indexgroup, self.plcAdr, self.plcDataType)

        if err:
            raise Exception(
                "error reading from address %i. error number %i" % (self.plcAdr, err)
            )
        if isinstance(self.guiObjects, (list, tuple)):
            for o in self.guiObjects:
                self.mapAdsToGui(o, value)
        else:
            self.mapAdsToGui(self.guiObjects, value)

        self.currentValue = value

        return value

    def mapAdsToGui(self, guiObject: HMIObject, value: VALUE_TYPE) -> None:
        """Display the value on the connected gui object.gui.

        This function should be overriden, by default the value is printed on the
        console.

        :param QObject guiObject: gui object for value output
        :param value: value to display in the gui object

        """
        print(value)
