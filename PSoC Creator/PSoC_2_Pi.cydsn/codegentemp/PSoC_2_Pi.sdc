# THIS FILE IS AUTOMATICALLY GENERATED
# Project: C:\Users\Brian\Dropbox\RPiSoC\Projects\PSoC_2_Pi\PSoC Creator\PSoC_2_Pi.cydsn\PSoC_2_Pi.cyprj
# Date: Tue, 26 Aug 2014 20:05:26 GMT
#set_units -time ns
create_clock -name {WaveDAC_clk(routed)} -period 4000 -waveform {0 2000} [list [get_pins {ClockBlock/dclk_1}]]
create_clock -name {ADC_DelSig_1_Ext_CP_Clk(routed)} -period 41.666666666666664 -waveform {0 20.8333333333333} [list [get_pins {ClockBlock/dclk_4}]]
create_clock -name {CyIMO} -period 333.33333333333331 -waveform {0 166.666666666667} [list [get_pins {ClockBlock/imo}]]
create_clock -name {CyPLL_OUT} -period 41.666666666666664 -waveform {0 20.8333333333333} [list [get_pins {ClockBlock/pllout}]]
create_clock -name {CyILO} -period 1000000 -waveform {0 500000} [list [get_pins {ClockBlock/ilo}] [get_pins {ClockBlock/clk_100k}] [get_pins {ClockBlock/clk_1k}] [get_pins {ClockBlock/clk_32k}]]
create_clock -name {CyMASTER_CLK} -period 41.666666666666664 -waveform {0 20.8333333333333} [list [get_pins {ClockBlock/clk_sync}]]
create_generated_clock -name {PWM_1_2_clk} -source [get_pins {ClockBlock/clk_sync}] -edges {1 25 49} [list [get_pins {ClockBlock/dclk_glb_0}]]
create_generated_clock -name {WaveDAC_clk} -source [get_pins {ClockBlock/clk_sync}] -edges {1 97 193} [list [get_pins {ClockBlock/dclk_glb_1}]]
create_generated_clock -name {PWM_7_8_clk} -source [get_pins {ClockBlock/clk_sync}] -edges {1 25 49} [list [get_pins {ClockBlock/dclk_glb_2}]]
create_generated_clock -name {PWM_5_6_clk} -source [get_pins {ClockBlock/clk_sync}] -edges {1 25 49} [list [get_pins {ClockBlock/dclk_glb_3}]]
create_clock -name {ADC_DelSig_1_Ext_CP_Clk} -period 41.666666666666664 -waveform {0 20.8333333333333} [list [get_pins {ClockBlock/dclk_glb_4}]]
create_generated_clock -name {PWM_3_4_clk} -source [get_pins {ClockBlock/clk_sync}] -edges {1 25 49} [list [get_pins {ClockBlock/dclk_glb_5}]]
create_generated_clock -name {Clock_3} -source [get_pins {ClockBlock/clk_sync}] -edges {1 3 5} [list [get_pins {ClockBlock/dclk_glb_6}]]
create_generated_clock -name {ADC_SAR_2_theACLK} -source [get_pins {ClockBlock/clk_sync}] -edges {1 3 5} [list [get_pins {ClockBlock/aclk_glb_0}]]
create_clock -name {ADC_SAR_2_theACLK(fixed-function)} -period 83.333333333333329 -waveform {0 41.6666666666667} [get_pins {ClockBlock/aclk_glb_ff_0}]
create_generated_clock -name {ADC_SAR_1_theACLK} -source [get_pins {ClockBlock/clk_sync}] -edges {1 3 5} [list [get_pins {ClockBlock/aclk_glb_1}]]
create_clock -name {ADC_SAR_1_theACLK(fixed-function)} -period 83.333333333333329 -waveform {0 41.6666666666667} [get_pins {ClockBlock/aclk_glb_ff_1}]
create_generated_clock -name {SPIS_1_IntClock} -source [get_pins {ClockBlock/clk_sync}] -edges {1 13 25} [list [get_pins {ClockBlock/dclk_glb_7}]]
create_generated_clock -name {ADC_DelSig_1_theACLK} -source [get_pins {ClockBlock/clk_sync}] -edges {1 39 77} [list [get_pins {ClockBlock/aclk_glb_2}]]
create_clock -name {ADC_DelSig_1_theACLK(fixed-function)} -period 1583.3333333333333 -waveform {0 791.666666666667} [get_pins {ClockBlock/aclk_glb_ff_2}]
create_generated_clock -name {CyBUS_CLK} -source [get_pins {ClockBlock/clk_sync}] -edges {1 2 3} [list [get_pins {ClockBlock/clk_bus_glb}]]
create_clock -name {CyBUS_CLK(fixed-function)} -period 41.666666666666664 -waveform {0 20.8333333333333} [get_pins {ClockBlock/clk_bus_glb_ff}]

set_false_path -from [get_pins {__ONE__/q}]

# Component constraints for C:\Users\Brian\Dropbox\RPiSoC\Projects\PSoC_2_Pi\PSoC Creator\PSoC_2_Pi.cydsn\TopDesign\TopDesign.cysch
# Project: C:\Users\Brian\Dropbox\RPiSoC\Projects\PSoC_2_Pi\PSoC Creator\PSoC_2_Pi.cydsn\PSoC_2_Pi.cyprj
# Date: Tue, 26 Aug 2014 20:04:36 GMT
