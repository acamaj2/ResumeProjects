/*Final program for Lab 4, with RTOS. 

Selects and plays one of 8 tunes, with name displayed on LCD                        */ 

 

#include "mbed.h" 

#include "tunes.h" 

#include "4bit_LCD.h" 

 

PwmOut speaker(D9);        //for piezo sounder (controls frequency and duty cycle of signal)

BusIn  choose(D3,D4,D5);   //for select buttons 

DigitalOut playing_led (D6);  //Led indicator 

DigitalOut ready_led (D7);    //Led indicator 

AnalogIn volume (A0);     //for potentiometer 

InterruptIn play(D2);     //for Play button 

 

Mutex lcd_mutex;  //protect code from concurency issues

 

//These flags indicate state of player 

bool welcome = 1;  //Indicates welcome state 

bool waiting = 0;  //waiting for tune selection 

bool primed = 0;   //tune is selected but hasn't started yet 

bool playing = 0;  //tune is playing 

 

void LCD_cont(void); 

void Tune_select(void); 

void Play_tune(void); 

 

//-------------- Threads ----------------// 

 

Thread thread1 ; //Displays welcome message on LCD 

void LCD_cont(void const *args){ 

    init_lcd();  //initialise the LCD 

//Waiting for song 

    while(1){ 

        if (welcome){ 

        lcd_mutex.lock(); 

        clr_lcd();   //Clear the LCD     

        print_lcd("Choose song"); 

        write_cmd(0xc0); //sets command mode of LCD

        print_lcd("Then press Play");  //Prints to LCD

        lcd_mutex.unlock(); 

        thread_sleep_for (500); 

        welcome=0; 

        ready_led=1; 

        }        //end of if 

    }            //end of while(1) 

} 

 

Thread thread2;         //Reads the select buttons and readies the song 

void Tune_select(void const *args){   

    while(1){ 

     if(primed){        //"primed" is set by Interrupt 

    switch(choose){     //read song selection and load song pointer 

        case 0x00:song_ptr=&Oranges;break; 

        case 0x01:song_ptr=&Cielito;break; 

        case 0x02:song_ptr=&Malaika;break; 

        case 0x03:song_ptr=&Guten_Abend;break; 

        case 0x04:song_ptr=&Yankee;break; 

        case 0x05:song_ptr=&Rasa;break; 

        case 0x06:song_ptr=&Matilda;break; 

        case 0x07:song_ptr=&Alouetta;break; 

        }              //end of switch 

      lcd_mutex.lock();      

      clr_lcd();   //Clear the LCD 

      print_lcd("Now playing:");   

      write_cmd(0xc0); 

      print_lcd(song_ptr->name);   //display song name 

      lcd_mutex.unlock(); 

      primed=ready_led=0; 

      playing=playing_led=1; 

      }  //end of if    

    } 

} 

 

Thread thread3;        //plays the chosen tune 

 void Play_tune(void const *args){ 

     while(1){ 

     if(playing){ 

        //resume PWM operation, stopped after last song 

        speaker.resume();       

        for (int i=0;i<=(song_ptr->length);i++) { 

          speaker.period(1/(2*(*song_ptr).freq[i]));   // set PWM period 

          speaker=volume;        // set duty cycle, hence volume control 

          thread_sleep_for(200*(*song_ptr).beat[i]); //hold for beat prd 

          } 

          //indicate end of song 

          playing_led=playing=false; 

          welcome=1; 

          speaker.suspend(); 

          }     //end of if 

        }       //end of while(1) 

 } 

 

void ISR(){      //responds to press of Play button, and sets "primed" 

    if(playing==0)  //only set "primed" if song not playing 

        primed=1; 

 } 

 

//--------------- Main ------------------// 

int main() { 

    ready_led=1; 

    play.fall(&ISR);  //Int. when Play is pressed, ie on falling edge 

    //Launch the threads 

    thread1.start(callback(LCD_cont,&playing_led)); 

    thread2.start(callback(Tune_select,&choose)); 

    thread3.start(callback(Play_tune,&play)); 

    while (1) {  

       __wfi();		//wait for interrupt 

    }   

} 