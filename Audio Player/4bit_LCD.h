/*Header file for a simple set of functions to write to 2x16 LCD, 

operating in 4-bit mode.                           */ 

 

#ifndef FOUR_BIT_LCD_H 

#define FOUR_BIT_LCD_H 

#include "mbed.h" 

#define ENABLE 0x08         //ORed in to data value to strobe E bit 

#define COMMAND_MODE 0x00   //to clear RS line to 0, for command transfer 

#define DATA_MODE 0x04      //to set RS line to 1, for data transfer 

 

//Function Prototypes 

void clr_lcd(void); 

void init_lcd(void); 

void print_lcd(const char *string); 

void shift_out(int data); 

void write_cmd(int cmd); 

void write_data(char c);  

void write_4bit(int data); 

#endif 