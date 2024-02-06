# UPS/Inverter charging controlled by Smart Plug

This project addresses the problem of charging a UPS against load-shedding when the UPS is on the downside of an existing solar-PV battery-inverter system.
Since the UPS has a relatively large battery of 200AH (12V) for a load of under 400W the UPS battery should not be charged from the primary battery. I.E. when it is load shedding. It should preferably be charged during the day when there is a Solar Surplus or when Grid power is available.


## Rules for operation

1. UPS should be used when load-shedding, thus the battery should be sufficiently charged before load-shedding.
2. UPS should be discharged up to 50% for regular cycling when possible and not conflict with rule 1.


## Status

- Rule 1 implemented.



## Python Modules

- tinytuya
- python-dotenv
- httpx
