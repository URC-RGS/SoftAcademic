1) установка armbian
    0) зажмите кнопку usb boot
    1) подключите одноплатник к пк (через ближний к краю платы usb разьем) 
    2) запустите программу RZ_USB_Boot_Helper_V1.0.0
    3) выберите в качестве файла для загрузки radxa-zero-erase-emmc.bin
    4) забустите запись (кнопка run)
    5) дождитесь пока закончиться запись и одноплатник стане определяться как usb накопитель 
    6) отворматируйте появившийся диск 
    7) запустите программу balenaEtcher-Setup-1.7.9
    8) выберете дистрибутиа линукса radxa-zero-ubuntu-focal-server-arm64-20211120-1315-mbr.img
    9) выбирите usb накопитель который вы отформатировали 
    10) запустите запись образа и дожитесь заверщения загрузки
    11) после завершения загрузки отсоедините от пк одноплатник 

2) установка софта 

    пользователь по умолчанию: rock
    пароль по умолчанию: rock

    sudo apt-get update

    0) если есть необходимость в подключении к WIFI

        nmcli r wifi on

        nmcli dev wifi

        (подключение к интернету общая структура комманды)
        sudo nmcli dev wifi connect "wifi_name" password "wifi_password"

        (у нас)
        sudo nmcli dev wifi connect URC-ROOT password 0987654321

        ifconfig

    1) скачивание репозитория 

        sudo apt install git-all

        git clone https://github.com/URC-RGS/SoftAcademic

    2) установка библиотеки для джойстика

        sudo apt install python3-pip

        sudo pip3 install pygame 

        sudo pip3 install pyserial

        sudo pip3 install coloredlogs

        sudo pip3 install verboselogs

    3) подключение джойстика 
         
        bluetoothctl

        power on 

        agent on
 
        default-agent

        # перевести джойстик в режим сопряжения

        scan on

        # надо найти джойскик и подставить его мак адрес в три команды ниже (без скобочек)
 
        pair <mac>
 
        connect <mac>
 
        trust <mac>

    4) включение uart

        sudo nano /boot/uEnv.txt

        # заменить следующие строки 
console=
overlays=meson-g12a-uart-ao-a-on-gpioao-0-gpioao-1 meson-g12a-uart-ao-b-on-gpioao-2-gpioao-3



    5) добавление в автозапуск 

        sudo apt-get install cron

        sudo crontab -e 

        1

        # добавить с конец файла

        @reboot sleep 5 && /usr/bin/python3 /home/rock/SoftAcademic/upperAcademic/Rov_pult.py &

    6) установка и синхранизация времени

        sudo timedatectl set-timezone Europe/Moscow

3) (опционально) настройка коэффицентов движителей
    # переходим в директорию с конфигом 

    cd SoftAcademic/raspberry-pult/

    # открываем конфиг для редактирования 

    sudo nano config_rov.ini

    # закрываем и сохраняем изменения 

    Ctrl + x
    y
    


