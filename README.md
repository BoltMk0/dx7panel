# dx7panel
Web-based UI for live sound editing on my DX7 so I don't have to use the cursed single slider interface..

![DX7Panel user interface](/screenshots/frontend.jpg?raw=true "DX7Panel User Interface")


The program is split into two components, both of which run on the same machine.

- Backend<br>
This is responsible for all communications to the DX7, and optionally from an extenal MIDI controller.
- Frontent<br>
This is a web server that is accessed from any device with a web browser on the network.

![DX7Panel user interface](/screenshots/workflow.drawio.png?raw=true "DX7Panel User Interface")

# Setup 
## Backend (AKA Server)

### Option 1: Running directly on the device
#### Requirements:
- Linux or Windows (MacOS doesn't work). Tested on a raspberry pi with Raspberry Pi OS Lite.
- Python 3 (Tested on 3.10)
    - Python3 modules: websockets rtmidi python-rtmidi pygame
- High quality MIDI interface capable of sysex messages (unfortunately cheap interfaces don't work). Tested with Roland UM-ONE Mk2 (Around $50)

#### Installation (Linux):
- Installing python: `sudo apt-get install python3 python3-pip`
- Installing python modules: `sudo pip3 install websockets rtmidi python-rtmidi pygame`
- Running the server (from this directory): `python3 -m server`

### Option 2: Running in docker
#### Requirements:
- Linux only. Tested on raspberry pi with Raspberry Pi OS Lite.
- High quality MIDI interface capable of sysex messages (unfortunately cheap interfaces don't work). Tested with Roland UM-ONE Mk2 (Around $50)

#### Installation:
- Install docker: `curl https://get.docker.com | sh` 
- Build the backend image: (While in the 'server' directory) `sudo docker build . -t dx7panel-backend`

#### Running:
```
sudo docker run -p 3000:3000 -v /dev:/dev --privileged --name dx7panel-backend --restart unless-stopped dx7panel-backend
```

## Frontend

### Option 1: Running directly on the device
#### Requirements: 
- Node 18+

#### Installation:
- Install node packages using npm: (While in the 'frontend' directory) `npm i`
- Build the server: `npm run build`

Changing the default port:<br>
By default the server build with a default port number of 3000. I recommend changing this to 80. <br>
Edit build/index.js, and change the line:
> const port = env('PORT', !path && '3000');

to

> const port = env('PORT', !path && '80');

Im sure there's a better way but it's not obvious to me.


#### Running:
```
node build/index.js
```

NOTE: by default this uses port 3000.

### Option 2: Running in docker
#### Installation:
- Install docker: `curl https://get.docker.com | sh`
- Build frontend image: (While in 'frontend' directory) `sudo docker build . -t dx7panel-frontend`

#### Running:<br>
```
sudo docker run -p 80:3000 --name dx7panel-frontend
```


# Operation Manual

I don't have time to document the entire UI, but the essentials:

## Configuring the MIDI I/O
Open a web browser, and navigate to `http://<dx7panel-host>/settings` (make sure you replace \<dx7panel-host\> with the IP address of the host running the frontend) and wait for the connection LED (top left corner) to turn green.

![DX7Panel settings](/screenshots/settings.jpg?raw=true "DX7Panel Settings")

- MIDI Input Device (Input)<br>
This isn't used for this application, but must be different from the thru device. Set this to "null"

- MIDI Output Device (Output)<br>
This is the output to the DX7. It must be a high quality MIDI interface (tested on the Roland UM ONE Mk2)

- MIDI Thru Device (Input)<br>
This is an optional device whos MIDI message will get passed through to the DX7.

- Velocity Correction <br>
The DX7 expects velocity in the range 0-100, most modern controllers give messages in the range 0-127. While this leads to some cool and whacky sounds, it's not always desirable. Check this checkbox to scale the velocity.

## Changing the default backend connection settings
By default, the fontend expects the backend to be available on the same address. If the frontend is running on a different host, you'll need to specify the IP address of the backend host.
- Click the colored circle ("Connection LED") in the top left of the page. Enter a new address in the form "\<ipaddress\>:\<port\>" and hit the return key to apply.

![DX7Panel connection settings](/screenshots/connection_settings.jpg?raw=true "DX7Panel Connection Settings")


