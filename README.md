# Sequential data processing with Deep Learning  : Retro gaming + TinyMachineLearning + PLN + VoiceRecognition

In this projects we are going to see different methods to use deep learning wiht   processing of sequential data .We have two folders:
 1) Lab2, using PLN with transformers and GPT. 
 2) Lab1, using voice recognition with deepLearning.
 You can see the results on each folder. But, In this post we are going to show you, how to set up our project.
 for getting our tinyMachineLearning - retro gaming. We code a SpaceInvader and test it. Let's see a little bit about it. We have the next topics:


⭐ MachineLearning + Gaming

⭐ Trainig/Testing a machine learning model

⭐ Coding a game

⭐ TinyMachine Learning

⭐ Deployment  & Integration


## MachineLearning + Gaming

Basicly, We want to set up a retro game, using some technologies of machine learning as an assets and physics interactions. As you'll know, as part of the teaching of artificial intelligent. Differents application's came up for making differents task and it's been applied in gaming. Now, we'll see this applications with embedded. Using platforms for tinyMachineLearning.

## Trainig/Testing a machine learning model

In this part what we want to define are the physics and the interactions with player and enviroment using machine learning. What we define is to use the basic concept of spaceship in a war with other spaceship. You know a space invader. So, the specific behaviour of our enviroment are the next topics:

* The player behaviour
* Enemy behaviour 
* Game interactions.

We focus on the player behaviour so, what we define were the movement of our player. We define the movement and the attacks methods and that is what we expect to control with machine learning. The use of enemies or their intelligences we'll be make it by symbolic methods. So let's define something. We want first 1) Move to left 2) Move to Right 3) Finally, Shoot. At least, in this first version, we'll code all the mechanical interactions but just train the last three mentioned before.

Now, what we're gonna process are sequential data, audio specially, we'll use two methods Spectograms, and MFCC
Theres more ways to do that however this is a good point of start.  We'll record audio of 1s saying our words, with a frequency rate of 16000. Left, right or shoot. Or wheter your want. 
We'll use espectogram and MFCC as we said as a inputs for our machine learning algorithm. We'll show a brief code and result, becaouse all code is in the folders.

----------

```python
# Espectogram
def preprocess(wave): 
    wav = wave[:16000]
    spectrogram = tf.signal.stft(wav, frame_length=255, frame_step=128)
    spectrogram = tf.abs(spectrogram)
    return spectrogram
```


```python
# MFCC
def preprocess(wave): 
    # Load wavefile
    signal, fs = librosa.load(wave, sr=16000)
    
    # Create MFCCs from sound clip
    mfccs = python_speech_features.base.mfcc(signal, 
                                            samplerate=fs,
                                            winlen=0.256,
                                            winstep=0.050,
                                            numcep=num_mfcc,
                                            nfilt=26,
                                            nfft=2048,
                                            preemph=0.0,
                                            ceplifter=0,
                                            appendEnergy=False,
                                            winfunc=np.hanning)
    
    return mfccs.transpose(), signal
```

----------

## Coding a Game

In this topic we'r gonna use some of OOP for our interactions. Firstly, we'll define a class with 
the differents attributes, and methods wich can be reused. For our player and our enemies.

```python
# Abstract entity game

class AbstractEntityGame:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None 
        self.lasers = []
        self.cool_down_counter = 0
        self.COOLDOWN = 30

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT_SCREEN):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x -3 , self.y - 55 , self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
            
    def get_width(self):
        return self.ship_img.get_width()
    def get_height(self):
        return self.ship_img.get_height()       


```
----------

## TinyMachine Learning

```C++
// Inference 
for (size_t ix = 0; ix < EI_CLASSIFIER_LABEL_COUNT; ix++) {
/* ei_printf("    %s: %.5f\n", result.classification[ix].label,
      result.classification[ix].value);*/
      
      if( result.classification[ix].label == "Derecha"){
        //Type 0: significa derecha 
        if(result.classification[ix].value > 0.70 ){
            send_command(0);
        }
        
      }

        if( result.classification[ix].label == "Izquierda"){
        //Type 1 siginifica izquierda 
        if(result.classification[ix].value > 0.70 ){
          send_command(1);
        }

      }
      if( result.classification[ix].label == "Fondo" ){
        //Type 2 siginifica fondo 
        if(result.classification[ix].value > 0.70 ){
          send_command(2);
        }

      }
      if( result.classification[ix].label == "Laser" ){
        //Type 3 siginifica laser 
        if(result.classification[ix].value > 0.70 ){
          send_command(3);
        }

      }

    }

```

----------

## Deployment  & Integration


```C++
// sending information
void send_command(int pred_index){
  switch (pred_index)
  {
    case 0:     // Derech:     
      Serial.print("derecha");
      break;

    case 1:     // Izquierda:       
      Serial.print("izquierda");
      break;
    
    case 2:     // Fondo:   
      Serial.print("fondo");
      break;
    case 3:     // laser:   
        Serial.print("laser");
        break;

  }
}
```


```python
#Arduino conecction
arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)

# Getting data
def get_arduino_data():   
    data = arduino.readline()
    return data

# Arduino data physics
def arduino_decision():
    NEXT_PLAYER_LEFT_X_POSITION = player.x - PLAYER_VEL
    NEXT_PLAYER_RIGHT_X_POSITION = player.x + PLAYER_VEL + player.get_width()
    
    word = get_arduino_data()
    word = codecs.decode(word, 'UTF-8')
    if(len(word) > 0):
        print(word)
        global NAV_IZQUIERDA
        global NAV_DERECHA
        global NAV_LASER
        if( word == 'izquierda'):
            NAV_IZQUIERDA = True
            NAV_DERECHA = False
            #NAV_LASER = False
        if(word == 'derecha'):
            NAV_DERECHA = True
            NAV_IZQUIERDA = False
            #NAV_LASER = False
        if(word == 'laser'):
            if(NAV_LASER):
                NAV_LASER = False
            else:
                NAV_LASER = True
                 

        if( NAV_IZQUIERDA and (NEXT_PLAYER_LEFT_X_POSITION > BEGIN_SCREEN)):
            player.x -= PLAYER_VEL
        if(NAV_DERECHA and (NEXT_PLAYER_RIGHT_X_POSITION < WIDTH_SCREEN)):
            player.x += PLAYER_VEL
        if(NAV_LASER):
            player.shoot()
```