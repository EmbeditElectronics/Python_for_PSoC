/*******************************************************************************
* File Name: GPIO_12_7.c  
* Version 2.0
*
* Description:
*  This file contains API to enable firmware control of a Pins component.
*
* Note:
*
********************************************************************************
* Copyright 2008-2014, Cypress Semiconductor Corporation.  All rights reserved.
* You may use this file only in accordance with the license, terms, conditions, 
* disclaimers, and limitations in the end user license agreement accompanying 
* the software package with which this file was provided.
*******************************************************************************/

#include "cytypes.h"
#include "GPIO_12_7.h"

/* APIs are not generated for P15[7:6] on PSoC 5 */
#if !(CY_PSOC5A &&\
	 GPIO_12_7__PORT == 15 && ((GPIO_12_7__MASK & 0xC0) != 0))


/*******************************************************************************
* Function Name: GPIO_12_7_Write
********************************************************************************
*
* Summary:
*  Assign a new value to the digital port's data output register.  
*
* Parameters:  
*  prtValue:  The value to be assigned to the Digital Port. 
*
* Return: 
*  None
*  
*******************************************************************************/
void GPIO_12_7_Write(uint8 value) 
{
    uint8 staticBits = (GPIO_12_7_DR & (uint8)(~GPIO_12_7_MASK));
    GPIO_12_7_DR = staticBits | ((uint8)(value << GPIO_12_7_SHIFT) & GPIO_12_7_MASK);
}


/*******************************************************************************
* Function Name: GPIO_12_7_SetDriveMode
********************************************************************************
*
* Summary:
*  Change the drive mode on the pins of the port.
* 
* Parameters:  
*  mode:  Change the pins to one of the following drive modes.
*
*  GPIO_12_7_DM_STRONG     Strong Drive 
*  GPIO_12_7_DM_OD_HI      Open Drain, Drives High 
*  GPIO_12_7_DM_OD_LO      Open Drain, Drives Low 
*  GPIO_12_7_DM_RES_UP     Resistive Pull Up 
*  GPIO_12_7_DM_RES_DWN    Resistive Pull Down 
*  GPIO_12_7_DM_RES_UPDWN  Resistive Pull Up/Down 
*  GPIO_12_7_DM_DIG_HIZ    High Impedance Digital 
*  GPIO_12_7_DM_ALG_HIZ    High Impedance Analog 
*
* Return: 
*  None
*
*******************************************************************************/
void GPIO_12_7_SetDriveMode(uint8 mode) 
{
	CyPins_SetPinDriveMode(GPIO_12_7_0, mode);
}


/*******************************************************************************
* Function Name: GPIO_12_7_Read
********************************************************************************
*
* Summary:
*  Read the current value on the pins of the Digital Port in right justified 
*  form.
*
* Parameters:  
*  None
*
* Return: 
*  Returns the current value of the Digital Port as a right justified number
*  
* Note:
*  Macro GPIO_12_7_ReadPS calls this function. 
*  
*******************************************************************************/
uint8 GPIO_12_7_Read(void) 
{
    return (GPIO_12_7_PS & GPIO_12_7_MASK) >> GPIO_12_7_SHIFT;
}


/*******************************************************************************
* Function Name: GPIO_12_7_ReadDataReg
********************************************************************************
*
* Summary:
*  Read the current value assigned to a Digital Port's data output register
*
* Parameters:  
*  None 
*
* Return: 
*  Returns the current value assigned to the Digital Port's data output register
*  
*******************************************************************************/
uint8 GPIO_12_7_ReadDataReg(void) 
{
    return (GPIO_12_7_DR & GPIO_12_7_MASK) >> GPIO_12_7_SHIFT;
}


/* If Interrupts Are Enabled for this Pins component */ 
#if defined(GPIO_12_7_INTSTAT) 

    /*******************************************************************************
    * Function Name: GPIO_12_7_ClearInterrupt
    ********************************************************************************
    * Summary:
    *  Clears any active interrupts attached to port and returns the value of the 
    *  interrupt status register.
    *
    * Parameters:  
    *  None 
    *
    * Return: 
    *  Returns the value of the interrupt status register
    *  
    *******************************************************************************/
    uint8 GPIO_12_7_ClearInterrupt(void) 
    {
        return (GPIO_12_7_INTSTAT & GPIO_12_7_MASK) >> GPIO_12_7_SHIFT;
    }

#endif /* If Interrupts Are Enabled for this Pins component */ 

#endif /* CY_PSOC5A... */

    
/* [] END OF FILE */
