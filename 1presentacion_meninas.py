# -*- coding: utf-8 -*-
import qi
from naoqi import ALProxy
import time

ip="192.168.174.85"
port=9559

# Proxies
movimiento = ALProxy("ALMotion", ip, port)
postura = ALProxy("ALRobotPosture", ip, port)
habla = ALProxy("ALTextToSpeech", ip, port)
animated_speech = ALProxy("ALAnimatedSpeech", ip, port)
leds = ALProxy("ALLeds", ip, port)


movimiento.wakeUp()
movimiento.setFallManagerEnabled(True)

# Anda hacia adelante
movimiento.moveTo(0.4, 0, 0)  

habla.say("Buenos días, mi nombre es NAO, encantado de conoceros. Hoy he venido para contaros mi historia.")

time.sleep(1)


# Sentarse
postura.goToPosture("StandInit", 1.0)
postura.goToPosture("Sit", 1.0)
time.sleep(2)


animated_speech.say("Soy un robot artista, pero hace un tiempo que no tengo inspiración. " \
"Todo ocurrió durante el apagón. Mi batería se acabó, y cuando desperté había perdido " \
"toda mi imaginación y cualidades artísticas. Incluso ahora, tengo que estar" \
"enchufado para poder funcionar bien...")

#Ojos azules
leds.fadeRGB("FaceLeds", 0x0000FF, 5) 

animated_speech.say(" Mi ayudante Paula y yo lo intentamos todo, incluso fuimos al médico, " \
"pero nos dijeron que allí solo atendían humanos")
animated_speech.say("Me sentí muy triste, e intenté todo lo que se me ocurrió para poder " \
"recuperarla, pero no hubo suerte, hasta que se me ocurrió pedir ayuda a los niños, que " \
"son los humanos que más imaginación tienen.")

# Levantarse
postura.goToPosture("StandInit", 1.0)
time.sleep(2)


animated_speech.say("Es por eso que mi ayudante y yo decidimos emprender un viaje por " \
"algunos colegios de Sevilla, para así poder pediros ayuda y poder recuperar mi " \
"imaginación para seguir pintando y dibujando toda la vida.")

animated_speech.say("Para ello, pensamos que sería bueno observar y entender " \
"algunas de mis obras de arte favoritas. Seguro que así empiezo a recordar, o eso espero...")

animated_speech.say("¿Qué me decís? Estáis dispuestos a ayudarme?")

# Ponerse la mano en la oreja
movimiento.setAngles("HeadYaw", 1.0, 0.2)
movimiento.setAngles("RShoulderPitch",0.5 , 0.2)  
movimiento.setAngles("RShoulderRoll", 0.75, 0.2)   
movimiento.setAngles("RElbowYaw", 0.95, 0.2)          
movimiento.setAngles("RElbowRoll", 1.57, 0.2)        
movimiento.setAngles("RWristYaw", 0.2, 0.2)          
movimiento.setAngles("RHand", 1.0, 0.2) 

animated_speech.say("No os oigo bien... Más alto, estáis dispuestos a ayudarme?")

postura.goToPosture("StandInit", 1.0)

time.sleep(3)

# Ojos verdes
leds.fadeRGB("FaceLeds", 0x00FF00, 5)  


animated_speech.say("No sabeis cuanto os lo agradezco. Entonces, empecemos!")

# Puño en alto
movimiento.setAngles("RShoulderPitch", -1, 0.2)   
movimiento.setAngles("RShoulderRoll", -0.2, 0.2)     
movimiento.setAngles("RElbowYaw", 1.5, 0.2)         
movimiento.setAngles("RElbowRoll", 0.3, 0.2)        
movimiento.setAngles("RHand", 0.0, 0.2)        

# Leds en color neutro
leds.fadeRGB("FaceLeds", 0xFFFFFF, 0.5)

# Relajarse
movimiento.rest()

