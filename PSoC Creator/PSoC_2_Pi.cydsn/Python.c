/* ========================================
 *
 * Copyright YOUR COMPANY, THE YEAR
 * All Rights Reserved
 * UNPUBLISHED, LICENSED SOFTWARE.
 *
 * CONFIDENTIAL AND PROPRIETARY INFORMATION
 * WHICH IS THE PROPERTY OF your company.
 *
 * ========================================
*/

#ifndef PYTHON_H
    #include "Python.h"
#endif

#ifdef USE_I2C
    uint8 WR_buf[I2C_BUFFER_SIZE]; 
    uint8 RD_buf[I2C_BUFFER_SIZE];
#endif

void Python_parser(vessel_type *vessel)
{
    uint8 cmd = vessel->cmd;
    uint8 addr = vessel->addr;
    uint16 temp_data;
    
    switch(addr)
    {
        //delsig_adc
        #ifdef CY_ADC_DELSIG_ADC_DelSig_1_H
            case DELSIG_ADC_CONTROL: break;
        #endif
        
        //sar adc 1
        #ifdef CY_ADC_SAR_ADC_SAR_1_H 
            case SAR_ADC0_CONTROL: break;
        #endif
        
        //sar adc 2
        #ifdef CY_ADC_SAR_ADC_SAR_2_H 
            case SAR_ADC1_CONTROL: break;
        #endif
        
        //VDAC1
        #ifdef CY_VDAC8_VDAC8_1_H
            case VDAC0_CONTROL: break;        
        #endif
        
        //VDAC2
        #ifdef CY_VDAC8_VDAC8_2_H
            case VDAC1_CONTROL: break;
        #endif
        
        //IDAC1
        #ifdef CY_IDAC8_IDAC8_1_H
            case IDAC0_CONTROL:  break;     
        #endif
        
        //IDAC2
        #ifdef CY_IDAC8_IDAC8_2_H
            case IDAC1_CONTROL: break;     
        #endif
        
        //Wave DAC
        #ifdef CY_WaveDAC8_WaveDAC8_1_H
            case WAVEDAC_CONTROL: break;      
        #endif
        
        //first PWM
        #ifdef CY_PWM_PWM_1_H
            case PWM_REGISTER0: break;
        #endif
        
        //second PWM
        #ifdef CY_PWM_PWM_2_H
            case PWM_REGISTER1: break;
        #endif
        
        //third PWM
        #ifdef CY_PWM_PWM_3_H
            case PWM_REGISTER2: break;
        #endif
        
        //fourth PWM
        #ifdef CY_PWM_PWM_4_H
            case PWM_REGISTER3: break;  
        #endif
        
        //fifth PWM
        #ifdef CY_PWM_PWM_5_H
            case PWM_REGISTER4: break;
        #endif
        
        //sixth PWM
        #ifdef CY_PWM_PWM_6_H
            case PWM_REGISTER5: break;  
        #endif
        
        //seventh PWM
        #ifdef CY_PWM_PWM_7_H
            case PWM_REGISTER6: break;
        #endif
        
        //eighth PWM
        #ifdef CY_PWM_PWM_8_H
            case PWM_REGISTER7:  break;
        #endif
        
        #ifdef CY_PWM_PWM_9_H
            case PWM_REGISTER8:  break;
        #endif
        
        #ifdef CY_PWM_PWM_10_H
            case PWM_REGISTER9:  break;
        #endif
        
        #ifdef CY_PWM_PWM_11_H
            case PWM_REGISTER10: break;
        #endif
        
        #ifdef CY_PWM_PWM_12_H
            case PWM_REGISTER11: break;
        #endif
        
        #ifdef CY_ADC_SAR_Seq_1_H
            case ANALOG_IN_REGISTER: break;
        #endif
        
        #ifdef CY_CAPSENSE_CSD_CapSense_1_H
            case CAPSENSE_REGISTER: break;
        #endif
        
        case GPIO_REGISTER: 
            temp_data    = vessel->dat;
            vessel->pin  = (temp_data>>1)&0x0007;
            vessel->port = (temp_data>>4)&0x000F;
            switch(cmd)
            {
                case 0x01: vessel->dat = temp_data&0x0001; break;
                case 0x03: vessel->dat = temp_data>>8&0x000F; break;
            }
        
        
            break;
        
        case CHECK_BUILD: break;
        
        case RESET_ADDRESS: break;
        
    }
}

void Python_Initialize(void)
{
        #if defined(USE_SPI)
            SPIS_1_Start();
            SPIS_1_ClearFIFO();
            SPIS_1_ClearRxBuffer();
            SPIS_1_ClearTxBuffer();

        #elif defined(USE_I2C)
            I2C_1_SlaveInitReadBuf(RD_buf,  I2C_BUFFER_SIZE);
            I2C_1_SlaveInitWriteBuf(WR_buf,  I2C_BUFFER_SIZE);
            I2C_1_Start();
        #endif
}

/****************************************************************************************//**
*  @brief receives 4 bytes of data from a Master Device, merges them into a 32 bit number, and
*         returns the result
*
*  @return: 32-bit number which contains all 4 bytes of transferred data, where the MSB is the 
            first item received.
*
*********************************************************************************************/
    
    void Python_getData(vessel_type *vessel)
    {   
        uint8 addr = 0;
        uint8 cmd = 0;
        uint8 dat_lo = 0;
        uint8 dat_hi = 0;
        
        /* SPI READ HANDLER */
        #if defined(USE_SPI)
            while(!SPIS_1_GetRxBufferSize()){/* Wait until the Rx buffer isn't empty */}
                addr = SPIS_1_ReadRxData();
    	    while(!SPIS_1_GetRxBufferSize()){/* Wait until the Rx buffer isn't empty */}
    	        cmd = SPIS_1_ReadRxData();
    	    while(!SPIS_1_GetRxBufferSize()){/* Wait until the Rx buffer isn't empty */}
    	        dat_lo = SPIS_1_ReadRxData();
            while(!SPIS_1_GetRxBufferSize()){/* Wait until the Rx buffer isn't empty */}
    	        dat_hi = SPIS_1_ReadRxData();
      
        /* I2C READ HANDLER */
        #elif defined(USE_I2C)
            while (!I2C_1_SlaveGetWriteBufSize()){}
            /* wait until I2C master is not writing or reading from the Buffer */
            while (!(I2C_1_SlaveStatus() & I2C_1_SSTAT_WR_CMPLT)){}         
                uint8 byteCount = I2C_1_SlaveGetWriteBufSize(); 
           
                addr = WR_buf[0];
                cmd = WR_buf[1];
                dat_lo = WR_buf[2];
                dat_hi = WR_buf[3];
                
                I2C_1_SlaveClearWriteStatus();
                I2C_1_SlaveClearWriteBuf();
                
        #endif
 
        vessel->addr = addr;
        vessel->cmd = cmd;
        vessel->dat = (dat_hi<<8)||dat_lo;
    }
    
/****************************************************************************************//**
*  @brief Writes data back to the Master device when appropriate. 
*
*  @param dat: 32-bit number which is to be sent to the Master device. It is split into 4
*              individual bytes, and transferred one at a time starting with the lowest byte
*
*********************************************************************************************/
    
    void Python_sendData(uint32 dat)
    {
            uint8 out_hi = (dat & 0xFF000000)>>24;
            uint8 out_mid_hi = (dat & 0x00FF0000)>>16;
            uint8 out_mid_lo = (dat & 0x0000FF00)>>8;
            uint8 out_lo = dat & 0x000000FF;
        
        /* SPI WRITE HANDLER */
        #if defined(USE_SPI)
            SPIS_1_ClearTxBuffer();
            SPIS_1_ClearFIFO();    //Clear the SPI buffers
            SPIS_1_ClearRxBuffer();
            
            uint8 SPI_buffer[3] = {out_mid_lo, out_mid_hi, out_hi};
            SPIS_1_WriteTxDataZero(out_lo);
            SPIS_1_PutArray(SPI_buffer, 3);
           
            while(!(SPIS_1_ReadTxStatus() & SPIS_1_STS_SPI_DONE)); //Wait until Tx buffer empties    
        
        /* I2C WRITE HANDLER */
        #elif defined(USE_I2C)
            while (I2C_1_SlaveGetReadBufSize()){}
            RD_buf[0] = out_lo;
            RD_buf[1] = out_mid_lo;
            RD_buf[2] = out_mid_hi;
            RD_buf[3] = out_hi;
            
            /*Wait until read is complete*/
            while (0u == (I2C_1_SlaveStatus() & I2C_1_SSTAT_RD_CMPLT)){}
                I2C_1_SlaveClearReadBuf();          /* Clear slave read buffer and status */
                (void) I2C_1_SlaveClearReadStatus();
        #endif
        
    }

/* [] END OF FILE */
