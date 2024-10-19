# Introduction
**This repository contains the materials for the workshop "Demystifying Bluetooth Low Energy with Python", presented at PyCon Portugal 2024.**

Ever wondered how Bluetooth Low Energy (BLE) works? Although it is a very ubiquitous technology, BLE requires a steep learning curve due to its complex architecture. In this workshop, we will demystify BLE, so you can support it in any Python application.

This workshop presents how Bluetooth Low Energy (BLE) works and what are the current tools and libraries that can be used to support BLE in Python applications.

The workshop will address the following aspects:

- Presentation of the the BLE architecture;
- Focus on the Generic Attribute Profile (GATT);
- Write clients to connect and retrieve data from BLE devices;
- Create a simple GATT server, where our client will connect.

The theoretical presentation of BLE is intertwined with practical examples using BLE tools and code examples. In the end of the workshop, you'll be able to add BLE support to your Python applications, as well as use Bluetooth tools to guide you during the development of a BLE applications.

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