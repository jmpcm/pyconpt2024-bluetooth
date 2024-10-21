# Introduction
**This repository contains the materials for the workshop "Demystifying Bluetooth Low Energy with Python", initially presented at PyCon Portugal 2024.**

Ever wondered how Bluetooth Low Energy (BLE) works? Although it is a very ubiquitous technology, BLE requires a steep learning curve due to its complex architecture. In this workshop, we will demystify BLE, so you can support it in any Python application.

This workshop presents how Bluetooth Low Energy (BLE) works and what are the current tools and libraries that can be used to support BLE in Python applications.

The workshop addresses the following aspects:

- Presentation of the the BLE architecture;
- Focus on the Generic Attribute Profile (GATT);
- Write a BLE Central to connect and retrieve data from BLE peripherals;
- Create a simple BLE GATT central.

The theoretical presentation of BLE is intertwined with practical examples using BLE tools and code examples. In the end of the workshop, you'll be able to add BLE support to your Python applications, as well as use Bluetooth tools to guide you during the development of a BLE applications.

**IMPORTANT:** the files in the repository might be modified, always with the intention of improving the workshop materials in the future. Please, visit the repository for any updates. Also, any contributions are more than appreciated!

# Preparation
Install the following packages:
```
pip install asyncio bleak bless
```

The exercises should work in an environment. Some convenience commands:
```
conda create --name ble && conda activate ble
````
```
mkdir ble && cd ble
python3 -m venv ble
source ble/bin/activate
```

# Repository structure
- `exercises`: Python files with the solution for the exercises proposed in the slides;
- `rpi_pico`: code for the Raspberry Pi Pico, that is used as the example device throughout the workshop. This is a VSCode project; installing the MicroPico extension is advisable;
- `slides`: file with the slides of the workshop. Currently, only available in PDF. The slides have been slightly modified to clarify some aspects that were addressed during the workshop, but were not written. 
The slides might be modified, in the future, to add more information, or fixing typos, missing references and/or links, etc.

# License

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/stefmolin/pandas-workshop">Demystifying Bluetooth Low Energy with Python</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://stefaniemolin.com">Jorge Miranda</a> is licensed under <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC BY-NC-SA 4.0<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/nc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/sa.svg?ref=chooser-v1" alt=""></a></p>

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg