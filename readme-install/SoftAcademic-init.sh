#!/bin/bash

# вывод теста в терминал 
echo "Hello installer SoftAcademic!"
# обновление всех репозиториев до актуальной версии 
sudo apt-get update
# установка необходимых инструментов 
sudo apt install git-all

sudo apt-get install cron
# клонирование репозитория с кодом 
git clone https://github.com/URC-RGS/SoftAcademic
# установка библиотек для питона 
sudo apt install python3-pip

sudo pip3 install pygame 

sudo pip3 install pyserial

sudo pip3 install coloredlogs

echo "SoftAcademic installation is complete!"