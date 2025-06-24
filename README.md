# tensistor_board_adm5

# расширение для работы с платой тензодатчиков 3д принтера flashforge adventurer 5m /pro , на внешнем хосте.
 Для работы понадобится 1 свободный трехвольтовый юарт или юсб-юарт свисток. в файле правите путь к последовательному (/dev/ttyS2) порту на свой.

 фаил закидываете по пути ~/klipper/klippy/extras

# В printer.cfg добавить строку  <br />
```shell

[send_get_tensistors_adm5]

```
<br />
# команды для работы: <br />
# H7 - узнать текущий вес <br />
# H1 - установить текущий вес как 0 <br />
# H2 - принять текущий вес как за груз в 500гр <br />
# H3 - установить значение срабатывания концевика <br />

<br />
@FishingSoulFT <br />
Улучшил код сделав вывод этих данных в веб интерфейс
<br />
в конфиг принтера нужно добавить секцию <br />

```shell
[temperature_sensor Ad5m_load_cell]
sensor_type: temperature_load
min_temp: -270
max_temp: 2048
```
<br />
# Сергей (ghzserg) (автор zmod) , полностью переработал расширение для его работы с принтерами серии AD5X , так же о нисправил критическую ошибку в моем расширении, ссылка на расширение https://github.com/ghzserg/zmod_ff5x/blob/1.5/.shell/zmod_tenz.py

В  конфиг вместо преведущего вариантов кода, нужно добавить 
```shell

[zmod_tenz]

[temperature_sensor weightValue]
sensor_type: temperature_load
min_temp: -273
max_temp: 2048

```
фаил закидываете по пути ~/klipper/klippy/extras

<br />

<br />

H7 возвращает данные с задержкой в 2 команды - я только учусь программировать питон.
распиновка датчика стоал на разъеме платы во вложенном рисунке
1) DET - эмулирует концевик
2) RES - сброс датчика
3) TX - передача данных
4) RX - прием данных
   скорость обмена 9600 бод
![pinout](https://github.com/VoronKor/tensistor_board_adm5/blob/main/tensistor_board_pinout.jpg)
