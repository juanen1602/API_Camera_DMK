# API_Camera_DMK
Codigo GNU/Linux y software para hacer peticiones a una camara DMK conectada a un servidor remoto mediante una API

##Version de linux
$ lsb_release -a
Distributor ID:	Raspbian
Description:	Raspbian GNU/Linux 9.4 (stretch)
Release:	9.4
Codename:	stretch

##Guia para realizar peticiones a traves de un cliente a un servidor
Esta guia indica, paso a paso, las instrucciones para lanzar una API que permita leer y modificar los parametros de una camara modelo DMK41AU02.AS. Para mas informacion acerca del Software: https://github.com/AlvaroConvilla/camera_DMK41AU02.AS
## Instalar Dependencias

```
# Build dependencias
sudo apt-get install git g++ cmake pkg-config libudev-dev libudev1 libtinyxml-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libglib2.0-dev libgirepository1.0-dev libusb-1.0-0-dev libzip-dev uvcdynctrl python-setuptools libxml2-dev libpcap-dev libaudit-dev libnotify-dev autoconf intltool gtk-doc-tools

# Runtime dependencias
sudo apt-get install gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly libxml2 libpcap0.8 libaudit1 libnotify4

sudo apt-get install libgtk-3-dev libnotify-dev
```

##Building API local
Para construir una API en modo servidor local

```
$ git clone https://github.com/juanen1602/API_Camera_DMK.git
$ cd API_Camera_DMK
$ python3 ApiRest.py
```

Para hacerle peticiones desde un explorador:

```
localhost:8080/
```

o tambien:

```
http://127.0.0.1:8080/
```

#Peticiones API

##Metodos GET:

```
localhost:8080/
```

Devuelve todos los parametros, las especificaciones tecnicas y el numero de modelo de la DMK.
Si queremos obteter solo los parametros:

```
localhost:8080/GetParameters
```
Nos dara una respuesta de este estilo:

```
{
  "Brightness": {
    "Category": "Exposure", 
    "Group": "Brightness", 
    "Value": {
      "CurrentValue": 0, 
      "DefaultValue": -8193, 
      "MaxValue": 63, 
      "MinValue": 0
    }
  }, 
  "Exposure": {
    "Category": "Exposure", 
    "Group": "Exposure", 
    "Value": {
      "CurrentValue": 33300, 
      "DefaultValue": 33300, 
      "MaxValue": -694967296, 
      "MinValue": 100
    }
  }, 
  "ExposureAuto": {
    "Category": "Exposure", 
    "Group": "Exposure", 
    "Value": {
      "CurrentValue": true, 
      "DefaultValue": false
    }
  }, 
  "Gain": {
    "Category": "Exposure", 
    "Group": "Gain", 
    "Value": {
      "CurrentValue": 260, 
      "DefaultValue": 57343, 
      "MaxValue": 1023, 
      "MinValue": 260
    }
  }, 
  "Gamma": {
    "Category": "Image", 
    "Group": "Gamma", 
    "Value": {
      "CurrentValue": 100, 
      "DefaultValue": 57343, 
      "MaxValue": 500, 
      "MinValue": 1
    }
  }
}
```

Si queremos un parametro en particular:

```
localhost:8080/GetParameters/Brightness
```

Nos dara una respuesta de este estilo:

```
{
  "Category": "Exposure", 
  "Group": "Brightness", 
  "Value": {
    "CurrentValue": 0, 
    "DefaultValue": -8193, 
    "MaxValue": 63, 
    "MinValue": 0
  }
}
```

Para la gamma, la ganancia, el tiempo de exposicion y el tiempo de exposicion automatico:

```
localhost:8080/GetParameters/Gamma
localhost:8080/GetParameters/Gain
localhost:8080/GetParameters/Exposure
localhost:8080/GetParameters/ExposureAuto
```

##Building API Remota
Para construir una API en modo servidor remoto.

```
$ sudo ifconfig
enxb827eb3cce30: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 169.254.184.179  netmask 255.255.0.0  broadcast 169.254.255.255
        inet6 fe80::7bd6:7bba:8bc:b653  prefixlen 64  scopeid 0x20<link>
        ether b8:27:eb:3c:ce:30  txqueuelen 1000  (Ethernet)
        RX packets 263  bytes 146773 (143.3 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 66  bytes 15751 (15.3 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 52  bytes 5870 (5.7 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 52  bytes 5870 (5.7 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

wlan0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.33  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::2629:2747:146e:2bd9  prefixlen 64  scopeid 0x20<link>
        ether b8:27:eb:69:9b:65  txqueuelen 1000  (Ethernet)
        RX packets 916  bytes 360820 (352.3 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 448  bytes 64255 (62.7 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

```

Si queremos comunicacion por ethernet, host = 169.254.184.179
Si queremos comunicacion por wifi (solo en redes de areas locales), host = 192.168.1.33

Cambiamos el codigo fuente con la direccion IP que deseamos, tal que asi:

```
app.run(host = '169.254.184.179', debug = True , port = 8080)
```

Si lo queremos con Ethernet.

```
app.run(host = '192.168.1.33', debug = True , port = 8080)
```

Si lo queremos con Wifi.

Ahora con la comunicación desde el cliente:

```
http://169.254.184.179:8080/
http://192.168.1.33:8080/
```

Se podrán hacer el mismo tipo de peticiones.
OJO! Solo puede haber comunicación entre cliente y servidor si ambos estan conectados a la misma Red.


