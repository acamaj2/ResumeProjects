/*A set of snips from international songs, mainly of around 8 bars. 

Each song is stored as a C structure.     */ 

 

//Define structure to hold songs 

struct Songs{    

char name[17];   //the song name 

int length;      //no of notes in song 

float freq[30];  //frequency array 

float beat[30];   //beat array 

}; 

 

struct Songs *song_ptr;  //points to selected song 

 

/*Note frequencies, for reference. 

mid C=262, D=294, E=330, F=349, F#=370, G=392, A=440, B=494,  

    C=523, C#=554, D=587, E=659, F=698 */ 

 

struct Songs Oranges={ 

.name="Oranges & Lemons", //England 

.length=11,         //enter number one less than no of notes 

.freq=659,554,659,554,440,494,554,587,494,659,554,440,  //frequencies 

.beat=2,2,2,2,2,1,1,2,2,2,2,4   //beat durations 

 }; 

 struct Songs Cielito={ 

.name="Cielito Lindo",  //Mexico 

.length=24, 

.freq=659,587,523,440,587,587,523,659,523,392,440,440,392,440,392,698,587,494,392,440,392,349,330,294,262,   

.beat=3,2,1,6,3,2,1,1,4,1,1,2,1,2,1,1,2,1,1,2,2,1,1,1,5,    

 }; 

 struct Songs Malaika={ 

.name="Malaika",       //Tanzania 

.length=19, 

.freq=294,494,494,440,494,523,440,370,392,392,294,494,494,440,494,523,440,370,392,392,   

.beat=2,4,6,1,1,1,2,1,4,6,2,4,6,1,1,1,2,1,4,6,    

 }; 

struct Songs Guten_Abend={   

.name="Guten Abend",  //Germany 

.length=26, 

.freq=370,370,440,370,370,440,370,440,588,554,494,494,440,330,370,392,330,330,370,392,330,392,554,494,440,554,587,  

.beat=1,1,3,1,1,4,1,1,2,3,1,2,2,1,1,2,2,1,1,4,1,1,1,1,2,2,4,    

 }; 

 struct Songs Yankee={ 

.name="Yankee Doodle",  //USA 

.length=28, 

.freq=392,392,440,494,392,494,440,294,392,392,440,494,392,370,294,392,392,440,494,523,494,440,392,370,294,330,370,392,392,  

.beat=1.0,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,    

 }; 

 struct Songs Rasa={ 

.name="Rasa Sayang",  //Malaysia 

.length=26, 

.freq=370,392,440,440,587,554,494,440,494,392,440,370,587,554,494,494,440,392,370,440,294,370,330,392,277,330,294,//frequency array 

.beat=1,1,2,2,2,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2    

 }; 

 struct Songs Matilda={ 

.name="Waltzing Matilda",  //Australia 

.length=20, 

.freq=554,554,494,494,440,494,554,440,370,415,440,330,440,554,660,660,660,660,660,660,660,  

.beat=2,2,2,2,1.5,0.5,1.5,0.5,1.5,0.5,2,2,1.5,0.5,2,1.5,0.5,2,1.5,0.5,4,    

 }; 

 struct Songs Alouetta={ 

.name="Alouetta",  //France 

.length=18,     

.freq=392,440,494,494,440,392,440,494,392,294,392,440,494,494,440,392,440,494,392,  

.beat=3,1,2,2,1.5,0.5,1.5,0.5,2,2,3,1,2,2,1.5,0.5,1.5,0.5,2,  

 }; 

/*A spare song! 

struct Songs Twinkle={ 

.name="Twinkle", 

.length=13, 

.freq=440,440,659,659,740,740,659,587,587,554,554,494,494,440,  //frequency array 

.beat=2,2,2,2,2,2,4,2,2,2,2,2,2,4,   //beat array 

 };*/ 