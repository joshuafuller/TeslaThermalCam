# Hardware Setup

This guide explains how to physically install the thermal camera system in your Tesla and ensure it has power and network connectivity.

## Mounting the Thermal Camera

1. **3D Printed Hood Mount**: Secure the camera using the provided 3D printed hood mount. The mount should be positioned so that the camera has a clear forward view while remaining firmly attached to the vehicle.
2. **Camera Connection**: Attach the P2 Pro thermal camera to a USB-A male to USB-C female extension cable. Route this cable from the mount into the frunk where the Raspberry Pi will be located.

## Required Cables

- **USB-A to USB-C Cable**: Used to connect the camera to the Raspberry Pi 5.
- **Optional Extension Cables**: Depending on your installation, you may want to add cable extensions to reach the Pi neatly from the mount location.

## Power Supply Options

The Raspberry Pi requires a stable 5V power supply. Two common approaches are:

1. **Tesla 12V Battery**: Use a 12V to 5V DC converter wired to the vehicle's 12V battery. This setup allows the Pi to draw power directly from the car.
2. **Standalone Battery Pack**: For quick testing or a removable setup, a USB power bank can supply the necessary 5V power.

Whichever option you choose, verify that the power source can provide at least 3A of current for the Raspberry Pi 5.

## Networking Setup

Connect the Raspberry Pi to a network so the video stream can be accessed in the car:

1. **Travel Router or Hotspot**: Place a travel router in the car and connect it to your phone's personal hotspot. Join the Raspberry Pi to this WiFi network.
2. **Direct Hotspot**: Alternatively, connect the Pi directly to your phone's hotspot or any other in-car WiFi source.

Once connected, the Pi will serve the thermal video stream over the network, which can then be viewed from the Tesla's browser.
