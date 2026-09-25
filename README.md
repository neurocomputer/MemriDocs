# Welcome to the Open Scientific Community for Memristor Research, In-Memory Computing, and Neuromorphic Systems!

This repository hosts documentation for our software tools, simulator, and systems for working with memristors.

## 📄 Publications

Information about our memristors has been published here:

> Mikhaylov, Alexey N., et al. "In-Memory Computing Enabled by 32× 8 1T1R Memristive Crossbar Arrays." *Electronics* 15.18 (2026): 4267. <https://doi.org/10.3390/electronics15184267>

## 🧪 Open Platform

The open platform project for working with memristive crossbar arrays is located in the following repository and will be published soon:

- <https://github.com/ai-systems-lab/MemArdBoard>

## 🛠 Software Stack

In our work we use three main programs:

1. **MemriBoard** — <https://github.com/neurocomputer/MemriBoard>

   A GUI application for memristor research, automated testing of crossbar arrays, and demonstration of RRAM and in-memory computing functionality. It also includes a simulator for memristors and for devices used to work with them.

2. **MemriCore** — currently a closed repository.

   Contains drivers for connecting various memristor-based devices and for their investigation in MemriBoard. If you are interested in working with real memristors, please let us know.

3. **MemriNeurons** — <https://github.com/neurocomputer/MemriNeurons>

   A framework for building neurons and neural networks on memristors and running them on our devices.

## 📁 Repository Structure

```
archive/              - zip archives of program code for those who don't know how to use GitHub
boards/               - instructions for working with devices and real memristors
examples/             - some usage examples
figures/              - images for documentation
writable_cells/       - experiment plans for finding working cells
                        (outdated, compatible with MemriBoard releases before September 2026 — needs updating!)
write_verify_tuning/  - experiment plans for programming conductances
                        (outdated, compatible with MemriBoard releases before September 2026 — needs updating!)
```

## 📚 Documentation

1. [`en_environment_setup.md`](en_environment_setup.md) — setting up the environment for working with the simulator and devices
2. [`en_xor_examples.md`](en_xor_examples.md) — description of simple examples of computing with memristors

Documentation for **MemriBoard** and **MemriNeurons** is provided inside those repositories. You can find links to it while reading `en_environment_setup.md`.

## 🎥 Video

|#|Description|Link|
|-|-|-|
|1|How to use the documentation|[Watch](https://disk.yandex.ru/i/zSH8-vFfje5UkA)|
|2|Environment setup|[Watch](https://disk.yandex.ru/i/L9obTbzNRVDmKw)|
|3|Memristor model|[Watch](https://disk.yandex.ru/i/4hBXaMO3bPY4QA)|
|4|Board simulator (mode_7, 9, mvm)|[Watch](https://disk.yandex.ru/i/oxjdxbnq5tepDA)|
|5|Reading and recording weights|[Watch](https://disk.yandex.ru/i/vKOrxC5DK3tAtg)|
|6|Multiplication and the dot product|[Watch](https://disk.yandex.ru/i/g9ZzDKtoI9Caog)|
|7|Creating a simple neuron|[Watch](https://disk.yandex.ru/i/b6FRC41qtTIURg)|
|8|Spiking neural networks|[Watch](https://disk.yandex.ru/i/v4yy50hzcfBupw)|
|9|LIF neurons and STDP|[Watch](https://disk.yandex.ru/i/zhefTyarE4NmiA)|
|10|Formal neural networks|[Watch](https://disk.yandex.ru/i/z5ZTtyi6XHFQyQ)|
|11|Keras2nmp converter|[Watch](https://disk.yandex.ru/i/ezZ2HuKMqAULPg)|

# 🚀 Enjoy exploring memristors!