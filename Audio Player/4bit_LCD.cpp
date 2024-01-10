/*A simple set of functions to write to 2x16 LCD, 

operating in 4-bit mode.                                        */ 

#include "4bit_LCD.h" 

 

DigitalOut CS(D10); 

SPI ser_port(D11, D12, D13); // Initialise SPI, using default settings 

 

void init_lcd(void){      //follow designated procedure in data sheet 

    thread_sleep_for (40); 

    shift_out(0x30);    //function set 8-bit 

    wait_us(37); 

    write_cmd(0x20);    //function set 

    wait_us(37); 

    write_cmd(0x20);    //function set 

    wait_us(37); 

    write_cmd(0x0C);    //display ON/OFF 

    wait_us(37); 

    write_cmd(0x01);    //display clear 

    wait_us(1520); 

    write_cmd(0x06);    //entry-mode set 

    wait_us(37); 

    write_cmd(0x28);    //function set 

    wait_us(37); 

} 

void write_4bit(int data, int mode){ //mode is RS line, cmd=0, data=1 

    int hi_n; 

    int lo_n; 

    hi_n = (data & 0xF0);  //form the two 4-bit nibbles that will be sent 

    lo_n = ((data << 4) &0xF0); 

//send each word twice, strobing the Enable line 

    shift_out(hi_n | ENABLE | mode);  

    wait_us(1); 

    shift_out(hi_n & ~ENABLE); 

    shift_out(lo_n | ENABLE | mode); 

    wait_us(1); 

    shift_out(lo_n & ~ENABLE); 

} 

void shift_out(int data){        //Sends word to SPI port 

    CS = 0; 

    ser_port.write(data); //Writes ASCII 8bit character

    CS = 1; 

} 

void write_cmd(int cmd){         //Configures LCD command word 

    write_4bit(cmd, COMMAND_MODE); 

} 

void write_data(char c){        //Configures LCD data word 

    write_4bit(c, DATA_MODE);    //1 for data mode 

} 

void clr_lcd(void){      //Clears display and waits required time 

    write_cmd(0x01);    //display clear 

    wait_us(1520); 

} 

void print_lcd(const char *string){  //Sends character string to LCD 

    while(*string) { 

        write_data(*string++); 

        wait_us(40); 

    } 

} 