"""
This module defines the usage for the analog functionality
of the RPiSoC.
"""

__author__ = 'Brian Bradley'
__version__ = '1.2.3'

from rpisoc import *
from time import sleep

class CapSense(object):
    """
    **Description:**
    Provides functionality for use of CapSense buttons on the RPiSoC. Define a CapSense object in the following
    way::
        My_capsense_button = CapSense(PIN)
    """
    def __init__(self,PIN, THRESHOLD = 0):
        """
        **Parameters:**

             - *PIN*: The capsense pin number. PIN n directly corresponds to the pin which you assign to Capsense_BTN_N in your rpisoc firmware
                    * The following is valid for the default version of the API (v1.2) which contains 6 capsense buttons
                        + The Cmod pin, which should be a 2.2nF capacitor, should be connected between ground and P4[6]
                        + PIN is the number relative to Port 4, between *0* and *5*.

        **Optional Parameters:**

            - *THRESHOLD*: The number of counts, between 0 and 255, which will be added to your calibrated baseline value to determine if a button has been touched.
                    * *0* means that the baseline value itself will be used as a comparison value. Generally, baseline + THRESHOLD is used
                    * The threshold may need to be high if the button data is noisy. Try printing the results of *readRaw()* to get an understanding of the output behavior as you touch the button, this will help determine a suitable value

        """
        if RPiSoC.CAPSENSE_SENSOR_NUM is 0:
            raise ValueError('Error: No CapSense pins found. Verify your schematic on the RPiSoC is correct, or try resetting the RPiSoC and trying again.')
        elif PIN not in range(RPiSoC.CAPSENSE_SENSOR_NUM):
            raise ValueError('Invalid CapSense sensor number chosen: Valid range is between 0 and %d'%(RPiSoC.CAPSENSE_SENSOR_NUM - 1))
        else:
            self.number = PIN
            self.address = RPiSoC.CAPSENSE_REGISTER
        self.threshold = THRESHOLD
    def Start(self):
        """
        **Description:**
            Initializes registers and enables active mode power template bits of the subcomponents used within CapSense. It also attempts to establish a CapSense baseline, which will be used as a comparison value in the *isTouched()* method.
            The button should not be touched when this method is called, otherwise the baseline value will be calibrated with a touched value. It will only set the baseline if it sees two identical readings in a row.
        """
        cmd = 0x00
        RPiSoC.commChannel.sendData((self.address,cmd))
        while True:
            self.baseline = self.readRaw()
            if self.baseline == self.readRaw():
                break


    def Stop(self):
        """
        **Description:**
            Disables component interrupts, and calls CapSense_ClearSensors() to reset all sensors to an inactive state.
        """
        cmd = 0x01
        RPiSoC.commChannel.sendData((self.address,cmd))

    def Sleep(self):
        """
        **Description:**
            Prepares the component for the device entering a low-power mode. Disables Active mode power template bits of the sub components used within CapSense, saves nonretention registers, and resets all sensors to an inactive state.
        """
        cmd = 0x02
        RPiSoC.commChannel.sendData((self.address,cmd))

    def Wakeup(self):
        """
        **Description:**
            Restores CapSense configuration and nonretention register values after the device wake from a low power mode sleep mode.
        """
        cmd = 0x03
        RPiSoC.commChannel.sendData((self.address,cmd))

    def Read(self):
        """
        **Description:**
            Gives the state of the capsense button, as determined by the PSoC firmware. This will need to be calibrated in the CapSense component for optimal results. Use isTouched for more general application.
        **Returns:**
            state: bool which represents the current state of the capsense button.
        """
        cmd = 0x18
        val = self.number
        return bool(RPiSoC.commChannel.receiveData((self.address,cmd, val),delay = 0.03))

    def readRaw(self):
        """
        **Description:**
            Gives an 8-bit raw value from the capsense raw data array. This is used to generate a baseline in *Start()*
        **Returns:**
            val: int which represents the raw value on the capsense button
        """
        cmd = 0x0F
        val = self.number
        return RPiSoC.commChannel.receiveData((self.address, cmd, val))

    def isTouched(self):
        """
        **Description:**
            Uses the calibrated baseline and provided threshold value to determine if the requested CapSense button is being touched
        """
        if self.readRaw()>(self.baseline + self.threshold):
            return True
        else:
            return False

class analogPin(object):
    """
    **Description:**
        Provides functionality for use of the analog pins exposed on the RPiSoC. Define an analogPin object in the following
        way::
            My_analog_pin = analogPin(PIN)
    """
    def __init__(self, PIN):
        """
        **Parameters:**

             - *PIN*: The analog pin number - This directly corresponds to the pins connected to your sequenced SAR ADC, where 0 is the top pin.
                    * The following is valid for the default version of the API (v1.2) which containts 8 analog pins.
                        + Valid arguments are between *0* and *7*
                        + PINs *0-7* are relative to Port 3. So PIN = 0 an analog pin on Port 3 Pin 0 (P3[0]), and PIN = 7 is on Port 3 Pin 7 (P3[7])
        """

        if int(PIN) not in range(RPiSoC.ANALOG_IN_NUM):
            raise ValueError('Invalid Pin for Analog input specified. Only %d analog inputs available.' %RPiSoC.ANALOG_IN_NUM)
        else:
            self.pin = PIN

        self.address = RPiSoC.ANALOG_IN_REGISTER
    def Read(self):
        """
        **Description:**
            Reads the specified analog pin
        **Returns:**
            Value in *counts* which represents the digital value after an A/D conversion on the specified pin. The voltage the is represented by the count value will depend on the resolution set by the SetResolution() method
        """
        cmd = 0x00
        counts = int(RPiSoC.commChannel.receiveData((self.address, cmd, self.pin)))
        return counts
    def ReadVolts(self, PRECISION = 2):
        """
        **Description:**
            Reads the specified analog pin and converts that digital reading to a voltage in Volts.

        **Optional Parameters:**
            *PRECISION:* The number of decimal points the voltage will be rounded to.
                    - The default value is 2, but precision up to 5 points is available.
        **Returns:**
            Value in *Volts* which is being applied to the specified analog pin. The resolution of the ADC does not affect this method; the conversion process accounts for the ADC resolution.
        """
        cmd = 0x01
        return round((float(((RPiSoC.commChannel.receiveData((self.address,cmd, self.pin)))/1000000.0))), PRECISION)

    def SetOffset(self,counts):
        """
        **Description:**
            Sets an offset on the ADC which is used by the CountsTo_Volts function. It will subtract the given offset before making the conversion.

        **Parameters:**
            - *offset*: ADC Value in *counts*, which will be used by the *CountsTo_Volts()* function by subtracting the given offset before making the conversion.

        """
        cmd = 0x02
        RPiSoC.commChannel.sendData((self.address, cmd, counts))

    def SetResolution(self, resolution):
        """

        **Description:**
            - This function sets the resolution of ALL analogPin objects. The resolution is defaulted to 12.

        **Parameters:**
            - *resolution:* An integer value, in bits, that represents the new resolution of the SAR ADC.
                * Valid entries are *8, 10, or 12.*

        **Side Effects:**
            - The ADC resolution cannot be changed during a conversion cycle. The recommended bestpractice is to stop conversions with *Stop()* before changint the resolution, and then restarting with *Start().* If you call *SetResolution()* during a conversion, the resolution will not change until the current conversion is complete. Data will not be available in the new resolution for another 6 + *resolution* clock cycles. You may need add a delay of this number of clock cycles after *SetResolution()* is called before data is valid again.
        """
        if resolution not in [8, 10, 12]:
            raise ValueError('Invalid resolution specified: valid entries are 8, 10, or 12')

        cmd = 0x03
        RPiSoC.commChannel.sendData((self.address, cmd, resolution))




class ADC(object):
    """
    **Description:**
        The ADC class provides functionality for using the Delta Sigma ADC and two
        Succesive Approximation ADC's on the RPiSoC. Define ADC objects in the following
        way::
                My_DELSIG    = ADC('DELSIG')
                My_SAR       = ADC('SAR0')
                My_other_SAR = ADC('SAR1')
    """

    def __init__(self, c_type):
        """
        **Paramaters:**
            *c_type:* The type of ADC to be used. Choose:
                - *DELSIG*
                - *SAR0*
                - *SAR1*

        **Note:**
            None of the ADCs are included by default in V1.2. You are able to add them by simply placing them in your schematic on your RPiSoC program.

        """

        self.type = c_type

        if self.type == 'DELSIG':
            if not RPiSoC.DELSIG:
                raise ValueError('Delta-Sigma ADC not found on PSoC Creator program, verify that it is in your schematic and named correctly')
            self.address = RPiSoC.DELSIG_ADC_CONTROL
        elif self.type == 'SAR0':
            if not RPiSoC.SAR0:
                raise ValueError('SAR0 ADC not found on PSoC Creator program, verify that it is in your schematic and named correctly')
            self.address = RPiSoC.SAR_ADC0_CONTROL
        elif self.type == 'SAR1':
            if not RPiSoC.SAR1:
                raise ValueError('SAR1 ADC not found on PSoC Creator program, verify that it is in your schematic and named correctly')
            self.address = RPiSoC.SAR_ADC1_CONTROL
        else:
            raise ValueError('Invalid ADC type: Choose "DELSIG" "SAR0" or "SAR1"')
        self.polarity = 1

        if RPiSoC.DEBUG:
            if self.address in RPiSoC.REGISTERS_IN_USE:
                print('WARNING: Attempting to initialize object at register %d which is already in use.' %self.address)
        RPiSoC.REGISTERS_IN_USE.append(self.address)

    def Start(self):
        """
        **Description:**
            Sets the initVar variable on the RPiSoC, calls the ADC_Init() function, and then calls the ADC_Enable() function. This function configures and powers up the ADC, but does not start conversions.
        """
        cmd = 0x00
        data = (self.address, cmd)
        RPiSoC.commChannel.sendData(data)

    def Stop(self):
        """
        **Description:**
            Disables and powers down the ADC
        """
        cmd = 0x01
        data = (self.address, cmd)
        RPiSoC.commChannel.sendData(data)

    def SetBufferGain(self, gain):
        """
        **Description:**
            Sets the input buffer gain.

        **Paramaters:**
            - *gain:* valid entries are *1, 2, 4,* or *8.* The output will be multiplied by this number

        **Side effects:** Increasing the gain will lower the buffer bandwidth
        """

        if self.type != 'DELSIG':
            raise ValueError('Setting Buffer Gain only supported by DELSIG ADC')

        cmd = 0x02

        if gain not in [1,2,4,8]:
            raise ValueError('Invalid Gain Value for DELSIG ADC: Accepts 1, 2, 4, or 8')

        data = (self.address, cmd, gain)
        RPiSoC.commChannel.sendData(data)

    def SetResolution(self, resolution):
        """

        **Description:**
            - This function sets the resolution of the SAR ADC's
            - *SetResolution()* is **not** valid for the DELSIG ADC, which is defaulted to 16 bits resolution.

        **Parameters:**
            - *resolution:* An integer value, in bits, that represents the new resolution of the SAR ADC.
                * Valid entries are *8, 10, or 12.*

        **Side Effects:**
            - The ADC resolution cannot be changed during a conversion cycle. The recommended bestpractice is to stop conversions with *StopConvert(),* change the resolution, then restart the conversions with *StartConvert().* If you decide not to stop conversions before calling this API, use *IsEndConversion()* to wait until conversion is complete before changing the resolution. If you call *SetResolution()* during a conversion, the resolution will not change until the current conversion is complete. Data will not be available in the new resolution for another 6 + *resolution* clock cycles. You may need add a delay of this number of clock cycles after *SetResolution()* is called before data is valid again.
        """

        if self.type == 'DELSIG':
            raise ValueError('Invalid operation for the DELSIG ADC; SetResolution is only used by the SAR ADC')

        if resolution not in [8, 10, 12]:
            raise ValueError('Invalid resolution specified: valid entries are 8, 10, or 12')

        cmd = 0x03
        RPiSoC.commChannel.sendData((self.address, cmd, resolution))

    def StartConvert(self):
        """
        **Description:**
            Forces the ADC to initialize a conversion. This is handled internally for the Delsig ADC, using the *Read()* function, but it is kept seperate for the SAR. It can be done seperately for the Delsig as well, if desired.
        """
        if self.type == "SAR0" or self.type == "SAR1":
            cmd = 0x04
        elif self.type == 'DELSIG':
            cmd = 0x03

        RPiSoC.commChannel.sendData((self.address, cmd))

    def StopConvert(self):
        """
        **Description:**
            Forces the ADC to end conversion. This is handled internally for the Delsig ADC, using the *Read()* function, but it is kept seperate for the SAR. It can be done seperately for the DELSIG as well, if desired.
        """
        if self.type == "SAR0" or self.type == "SAR1":
            cmd = 0x05
        elif self.type == 'DELSIG':
            cmd = 0x04

        RPiSoC.commChannel.sendData((self.address,cmd))

    def GetResult(self):
        """
        **Description:**
            This function will get the result of a conversion which has been completed. *StartConvert()* must be called prior to this function, and *StopConvert()* must be called after.

        **Returns:**
            Value in *counts* of the most recent A/D conversion.
        """

        cmd = 0x0A
        counts = int(RPiSoC.commChannel.receiveData((self.address, cmd)))

        if counts<0:
            self.polarity = -1
        else:
            self.polarity = 1

        return counts


    def Read(self):
        """
        **Description:**
            This function simplifies the reading process by starting conversion, waiting for conversion to complete, stopping conversion, and returing the result, when called. It is only valid for the *DELSIG*

        **Returns:**
            Value in *counts* of the most recent A/D conversion.
        """
        if self.type != 'DELSIG':
            raise ValueError('Read function is only valid for the DELSIG ADC')

        cmd = 0x0D

        counts = int(RPiSoC.commChannel.receiveData((self.address, cmd)))

        if counts<0:
            self.polarity = -1
        else:
            self.polarity = 1

        return counts

    def IsEndConversion(self):
        """
        **Description:**
            This function checks to see if the ADC is done converting.

        **Returns:**
            - The value of the most recent conversion, if it is complete.
            - *0* if the conversion is not complete
        """
        if self.type == 'DELSIG':
            cmd = 0x07
        elif self.type == "SAR0" or self.type == "SAR1":
            cmd = 0x08

        return int(RPiSoC.commChannel.receiveData((self.address,cmd)))

    def SetOffset(self, offset):
        """
        **Description:**
            Sets an offset on the ADC which is used by the CountsTo_Volts function. It will subtract the given offset before making the conversion.

        **Parameters:**
            - *offset*: ADC Value in *counts*, which will be used by the *CountsTo_Volts()* function by subtracting the given offset before making the conversion.

        """
        if self.type == 'DELSIG':
            cmd = 0x0E
        elif self.type == "SAR0" or self.type == "SAR1":
            cmd = 0x0B

        RPiSoC.commChannel.sendData((self.address,cmd, offset))

    def SetGain(self, gain):
        """
        **Description:**
            Sets the ADC *gain* in counts per volt for the *CountsTo_Volts()* function.

        **Parameters:**
           - *gain:* Output gain in counts per volt to be applied before conversion.

        **Warning:**
            *gain* is set by default by the reference and input range settings. It should only be used to further calibrate the ADC with a known input or if an external reference is used.
        """

        if self.type == 'DELSIG':
            cmd = 0x0F
        elif self.type == "SAR0" or self.type == "SAR1":
            gain*=10 #SAR takes gain in counts per 10 volts
            cmd = 0x0C

        RPiSoC.commChannel.sendData((self.address,cmd, gain))

    def CountsTo_Volts(self, counts):
        """
        **Description:**
            Converts the ADC output to a Voltage.

        **Returns:**
            A float which represents the converted count number in Volts.
        """
        if self.type == 'DELSIG':
            cmd = 0x10
        elif self.type == "SAR0" or self.type == "SAR1":
            cmd = 0x0D

        counts*=self.polarity
        counts = int(counts)
        return self.polarity*(float(((RPiSoC.commChannel.receiveData((self.address,cmd, counts)))/1000000.0)))

    def Sleep(self):
        """
        **Description:**
            The ADC Sleep function checks to see if the component is enabled, then it stops the ADC and saves the current configuration for later use.
        """
        if self.type == 'DELSIG':
            cmd = 0x14
        elif self.type == "SAR0" or self.type == "SAR1":
            cmd = 0x10

        RPiSoC.commChannel.sendData((self.address,cmd))

    def Wakeup(self):
        """
        **Description:**
            The ADC Wakeup function restores the most recently saved ADC configuration so that it can be restarted.
        """
        if self.type == 'DELSIG':
            cmd = 0x15
        elif self.type == "SAR0" or self.type == "SAR1":
            cmd = 0x11

        RPiSoC.commChannel.sendData((self.address,cmd))

class IDAC(object):
    """
    **Description:**
        The IDAC class provides functionality for using the IDAC's available on the RPiSoC. Define IDAC objects in the following
        way::
            My_IDAC       = IDAC(0)
            My_other_IDAC = IDAC(1)

    """
    def __init__(self, channel):
        """

        **Parameter:**

            - *channel* Determines which IDAC is the be utilized
                * *0* for the first IDAC; output is on P0[7] by default
                * *1* for the second IDAC; not available by default


        """
        self.channel = channel

        if self.channel == 0:
            if not RPiSoC.IDAC0:
                raise ValueError('IDAC0 not found on PSoC Creator program, verify that it is in your schematic and named correctly')
            self.address = RPiSoC.IDAC0_CONTROL
            self.full_range = RPiSoC.IDAC0_RANGE
       	elif self.channel == 1:
            if not RPiSoC.IDAC1:
                raise ValueError('IDAC1 not found on PSoC Creator program, verify that it is in your schematic and named correctly')
            self.address = RPiSoC.IDAC1_CONTROL
            self.full_range = RPiSoC.IDAC1_RANGE
        else:
            raise ValueError('Invalid channel: Only two IDACs available; choose 0 or 1.')

        if RPiSoC.DEBUG:
            if self.address in RPiSoC.REGISTERS_IN_USE:
                print('WARNING: Attempting to initialize object at register %d which is already in use.' %self.address)
        RPiSoC.REGISTERS_IN_USE.append(self.address)


    def Start(self):
        """
        **Description:**
            Sets the initVar variable on the RPiSoC, calls the IDAC8_Init() function and then calls the IDAC8_Enable() function. Enables and powers up the IDAC
        """
        cmd = 0x00
        RPiSoC.commChannel.sendData((self.address, cmd))

    def Stop(self):
        """
        **Description:**
            Powers down IDAC to lowest power state and disables output.
        """
        cmd = 0x01
        RPiSoC.commChannel.sendData((self.address, cmd))

    def SetSpeed(self,speed):
        """
        **Description:**
            Sets the DAC speed, and consequently the power level.

        **Parameters:**
            - speed: *HIGH* or *LOW*
                * *HIGH* speed puts the DAC in high power mode
                * *LOW* speed puts the DAC in low power mode.
        """
        cmd = 0x02
        if speed =='LOW':
            val = 0
        elif speed =='HIGH':
            val = 1
        else:
            raise ValueError('Invalid Speed: Input "HIGH" or "LOW"')

        RPiSoC.commChannel.sendData((self.address, cmd, val))

    def SetPolarity(self,polarity):
        """
        **Description:**
            Sets the DAC output polarity.

        **Parameters:**
            *polarity:* *SOURCE* or *SINK*
        """

        cmd = 0x03
        if polarity =='SOURCE':
            val = 0
        elif polarity =='SINK':
            val = 1
        else:
            raise ValueError('Invalid Polarity: Input "SOURCE" or "SINK"')

        RPiSoC.commChannel.sendData((self.address, cmd, val))


    def SetRange(self, mode):
        """
        **Description:**
            Sets the Full scale range for the IDAC

        **Parameter:**
            - *mode:* *0, 1, or 2*
                * *0*: Sets full scale range to **31.875 uA**
                * *1*: Sets full scale range to **255 uA**
                * *2*: Sets full scale range to **2.04 mA**
        """
        cmd = 0x04
        if mode not in range(3):
            raise ValueError('Invalid Mode Specified:\n"0" for 32uA range\n"1" for 255uA range\n"2" for 2mA range ')
        if mode == 0:
            self.full_range = .031875
        elif mode == 1:
            self.full_range = .255
        elif mode == 2:
            self.full_range = 2.04

        RPiSoC.commChannel.sendData((self.address, cmd, mode))


    def SetValue(self, value):
        """
        **Description:**
            Sets value to output on IDAC. Valid values are between 0 and 255.

        **Parameters:**
            - *value*: number between 0 and 255.
                 * A value of 0 is the lowest and a value of 255 is the full-scale value.
                     + The full-scale value depends on the range, which is selected with SetRange()
        """
        cmd = 0x05
        if value not in range(256):
            raise ValueError('Invalid IDAC Value: Input integer values between 0(min) and 255(max)')

        RPiSoC.commChannel.sendData((self.address, cmd, value))

    def SetCurrent(self, amps):
        """
        **Description:**
        Sets a current in milliamps to be output on the specified IDAC. Valid values depend on the chosen full scale range

        **Parameters:**
        - *amps*: number between 0 and the full scale range in milliamperes.
        * The full scale value depends on the range, which is chosen with the SetRange() method.
        """

        if amps <= self.full_range and amps>=0:
            digital_val = int((float(amps)/self.full_range) * 255 + 0.5)
        else:
            digital_val = int(255*(amps>self.full_range))

        self.SetValue(digital_val)


    def Sleep(self):
        """
        **Description:**
            The IDAC Sleep function checks to see if the component is enabled, then it stops the IDAC and saves the current configuration for later use.
        """
        cmd = 0x06
        RPiSoC.commChannel.sendData((self.address, cmd))

    def Wakeup(self):
        """
        **Description:**
            Restores the most recently saved IDAC configuration so that it can be restarted.
        """
        cmd = 0x07
        RPiSoC.commChannel.sendData((self.address, cmd))

class VDAC(object):
    """
    **Description:**
        The VDAC class provides functionality for using the VDAC's available on the RPiSoC. Define VDAC objects in the following
        way::
            My_VDAC       = VDAC(0)
            My_other_VDAC = VDAC(1)
    """
    def __init__(self, channel):
        """

        **Parameters:**

            - *channel:* Determines which VDAC is to be utilized
                * *0* for the first VDAC; output is on P0[1] by default
                * *1* for the second VDAC; not available by default
        """

        self.channel = channel

        if self.channel == 0:
            if not RPiSoC.VDAC0:
                raise ValueError('VDAC0 not found on PSoC Creator program, verify that it is in your schematic and named correctly')
            self.address = RPiSoC.VDAC0_CONTROL
            self.full_range = RPiSoC.VDAC0_RANGE
        elif self.channel == 1:
            if not RPiSoC.VDAC1:
                raise ValueError('VDAC1 not found on PSoC Creator program, verify that it is in your schematic and named correctly')
            self.address = RPiSoC.VDAC1_CONTROL
            self.full_range = RPiSoC.VDAC1_RANGE
        else:
            raise ValueError('Invalid channel: Only two VDACs available; choose 0 or 1')

        if RPiSoC.DEBUG:
            if self.address in RPiSoC.REGISTERS_IN_USE:
                print('WARNING: Attempting to initialize object at register %d which is already in use.' %self.address)
        RPiSoC.REGISTERS_IN_USE.append(self.address)

    def Start(self):
        """
        **Description:**
            Sets the initVar variable on the RPiSoC, calls the VDAC8_Init() function and then calls the VDAC8_Enable() function. Enables and powers up the IDAC
        """
        cmd = 0x00
        RPiSoC.commChannel.sendData((self.address, cmd))

    def Stop(self):
        """
        **Description:**
            Powers down the VDAC to lowest power state and disables output.
        """
        cmd = 0x01
        RPiSoC.commChannel.sendData((self.address, cmd))

    def SetSpeed(self,speed):
        """
        **Description:**
            Sets the DAC speed, and consequently the power level.

        **Parameters:**
            *speed:* *HIGH* or *LOW*
                - *HIGH* speed puts the DAC in high power mode
                - *LOW* speed puts the DAC in low power mode
        """
        cmd = 0x02
        if speed =='LOW':
            val = 0
        elif speed =='HIGH':
            val = 1
        else:
            raise ValueError('Invalid Speed: Input "HIGH" or "LOW"')

        RPiSoC.commChannel.sendData((self.address, cmd, val))

    def SetRange(self,Range):
        """
        **Description:**
            Sets the Full scale range for the IDAC

        **Parameters:**
            *Range:* *HIGH* or *LOW*
                - *HIGH:* Sets full scale range to **4.080V**
                - *LOW :* Sets full scale range to **1.020V**
        """
        cmd = 0x03
        if Range =='LOW': #Range of 1.020 V
            val = 0
            self.full_range = 1.02
        elif Range =='HIGH': #Range of 4V
            val = 1
            self.full_range = 4.08
        else:
            raise ValueError('Invalid Range: Input "HIGH" for 4.080V range or "LOW" for 1.020V range')

        RPiSoC.commChannel.sendData((self.address, cmd, val))

    def SetVoltage(self, volts):
        """
        **Description:**
        Sets a voltage in Volts to be output on the specified VDAC. Valid values depend on the chosen full scale range

        **Parameters:**
        - *volts*: number between 0 and the full scale range in Volts.
        * The full scale value depends on the range, which is chosen with the SetRange() method.
        """


        if volts <= self.full_range and volts>=0:
            digital_val = int((float(volts)/self.full_range) * 255 + 0.5)
        else:
            digital_val = int(255*(volts>self.full_range))
        self.SetValue(digital_val)

    def SetValue(self, value):
        """
        **Description:**
            Sets value to output on VDAC.

        **Parameters:**
            *value:* integer between *0* and *255.*
                - A value of *0* is the lowest and a value of *255* is the full-scale value.
                    * The full-scale value depends on the range, which is selected with SetRange()
        """
        cmd = 0x04
        if value not in range(256):
            raise ValueError('Invalid VDAC Value: Input values between 0(min) and 255(max)')

        RPiSoC.commChannel.sendData((self.address, cmd, value))


    def Sleep(self):
        """
        **Description:**
            Checks to see if the component is enabled, then it stops the VDAC and saves the current configuration for later use.
        """
        cmd = 0x05
        RPiSoC.commChannel.sendData((self.address, cmd))

    def Wakeup(self):
        """
        **Description:**
            Restores the most recently saved VDAC configuration so that it can be restarted.
        """

        cmd = 0x06
        RPiSoC.commChannel.sendData((self.address, cmd))

class WaveDAC(object):
    """
    **Description:**
        The WaveDAC class provides functionality for using the WaveDAC available on the RPiSoC. Define WaveDAC objects in the following
        way::
            My_Wave = WaveDAC()
    """

    def __init__(self):

        if not RPiSoC.WAVEDAC:
                raise ValueError('Wave DAC not found on PSoC Creator program, verify that it is in your schematic and named correctly')
        self.master_clk = 3000000 #might want to automate....
        self.frequency = 250000
        self.divider_value = 12
        self.amplitude = 255
        self.dcBias = 0
        self.waveType = 'SINE'
        self.address = RPiSoC.WAVEDAC_CONTROL

        if RPiSoC.DEBUG:
            if self.address in RPiSoC.REGISTERS_IN_USE:
                print('WARNING: Attempting to initialize object at register %d which is already in use.' %self.address)
        RPiSoC.REGISTERS_IN_USE.append(self.address)

    def Start(self):
        """
        **Description:**
            Performs all of the required initialization for the component and enables power to the block.
            The first time the routine is executed, the range, polarity (if any), and power (speed)
            settings are configured for the operating mode selected in the design. When called to
            restart the WaveDAC8 following a Stop() call, the current component parameter settings are retained.
        """
        cmd = 0x00
        RPiSoC.commChannel.sendData((self.address, cmd))

    def Stop(self):
        """
        **Description:**
            Turn off the WaveDAC8 block.
        """
        cmd = 0x01
        RPiSoC.commChannel.sendData((self.address, cmd))

    def SetSpeed(self, speed):
        """
        **Description:**
            Sets the drive mode / speed to one of the settings.

        **Parameters:**
            *speed:* *HIGH* or *LOW*
                - *HIGH :* Highest power and fastest slew rate
                - *LOW  :* Lowest active power and slowest slew rate

        """
        cmd = 0x07

        if speed == 'HIGH':
            val = 1
        elif speed == 'LOW':
            val = 0
        else:
            raise ValueError('Invalid Speed: Choose "HIGH" or "LOW"')


        RPiSoC.commChannel.sendData((self.address, cmd, val))

    def Generate_Wave(self, waveType):
        """
        **Description:**
            Provides functionality for generating a specific waveform. It uses the class attributes *self.amplitude* and *self.dcB,* which define
            the waveforms peak voltage and the DC Bias, respectively. These are defaulted to 4V amplitude and 0V DC Bias, unless modifed by using the *setAmplitude()* and *setdcBias()* functions.

        **Parameters:**
               - *waveType:* string
                    * *SINE*
                    * *SQUARE*
                    * *TRIANGLE*
                    * *SAWTOOTH*

        **Note:** *V1.3* intends to introduce defining your own custom waveforms.
        """

        cmd = 0x04
        self.waveType = waveType

        if waveType == 'SINE':
            val = 0x01
        elif waveType =='SQUARE':
            val = 0x03
        elif waveType == 'TRIANGLE':
            val = 0x05
        elif waveType == 'SAWTOOTH':
            val = 0x07
        else:
            raise ValueError('Invalid waveType: Choose "SINE" "SQUARE" "TRIANGLE" or "SAWTOOTH" ')

        RPiSoC.commChannel.sendData((self.address, cmd))
        RPiSoC.commChannel.sendData((val, self.amplitude, self.dcBias))


    def SetValue(self, val):
        """
        **Description:**
            Sets the output of the DAC to the desired value. It is preferable to use this function when
            the clock is stopped. If this function is used during normal operation (clock is running), the
            predefined waveform may be interrupted.

        **Parameters:**
            - *val:* 8-bit DAC value between *0* and *255*
        """
        cmd = 0x09
        if val not in range(256):
            raise ValueError('Invalid WaveDAC Value: Input integer between 0(min) and 255(max)')
        else:
            RPiSoC.commChannel.sendData((self.address,cmd,val))

    def Sleep(self):
        """
        **Description:**
            Checks to see if the component is enabled, then it stops the WaveDAC and saves the current configuration for later use.
        """
        cmd = 0x0B
        RPiSoC.commChannel.sendData((self.address, cmd))

    def Wakeup(self):
        """
        **Description:**
            Restores the most recently saved WaveDAC configuration so that it can be restarted.
        """
        cmd = 0x0C
        RPiSoC.commChannel.sendData((self.address, cmd))


    def SetFrequency(self, frequency):
        """
        **Description:**
            Sets an approximate frequency by using an appropriate clock divider so that the resulting wave is as close to the desired frequency as possible.

        **Parameters:**
            - *frequency:* A frequency in Hz between *0* and *2500.*
        """
        cmd = 0xFF

        if frequency > 2500:
            print("WARNING: Wave Frequency cannot be greater than 2.5kHz \nWave frequency will be set to 2.5kHz to prevent runtime errors.")
            frequency = 2500
        elif frequency<0.46:
            print('WARNING: Wave Frequency must not be less than 0.46 Hz because no valid clock divider will sufficiently achieve such a frequency. Frequency will be set to 0.46 Hz to prevent runtime errors ')
            frequency = 0.46

        divider = int((self.master_clk/(frequency*100.0)) + 0.5)
        self.divider_value = (RPiSoC.commChannel.receiveData((self.address, cmd, divider))) + 1

    def GetFrequency(self):
        """
        **Description:**
            Calculates the actual wave frequency based on the most recently confirmed clock divider value.

        **Returns:**
            The *actual* frequency of the wave, *not* of the requested frequency.
        """
        return int(((self.master_clk/self.divider_value)/100.0))

    def StartClock(self):
        """
        **Description:**
            Restarts the WaveDAC clock after it has been stopped.
        """
        cmd = 0xFD
        RPiSoC.commChannel.sendData((self.address,cmd))

    def StopClock(self):
        """
        **Description:**
            Stops the WaveDAC clock so that a value can be set without interference by the clock.
        """
        cmd = 0xFE
        RPiSoC.commChannel.sendData((self.address,cmd))

    def setAmplitude(self, amplitude):
        """
        **Description:**
            Modifies the class attribute associated with peak voltage of a generated wave.

        **Parameters:**
            - *amplitude:* a peak amplitude, in Volts, between *0* and *4.*
                * The amplitude can be greater than 4V, but the output will saturate at 4.080 V.
        """
        self.amplitude = int(255/4.0*float(amplitude))

    def setdcBias(self, dcBias):
        """
        **Description:**
            Modifies the class attribute associated withthe DC Bias of a generated wave.

        **Parameters:**
            - *dcBias:* a DC Bias, in Volts, between *0* and *4.*
                * The generated wave will be offset by this amount.
                * The DC Bias can be greater than 4 Volts, but the output will saturate at 4.080 V.
        """
        self.dcBias = int(255/4.0*float(dcBias))


