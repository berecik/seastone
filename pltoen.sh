#!/usr/bin/env bash


sed -i 's/Zwolnienie miejsca/Releasing the berth/g' templates/add_leave.html

sed -i 's/Miejsce będzie do dyspozycji mariny:/The berth will be manage by marina:/g' templates/add_leave.html

sed -i 's/Data Od/Date from/g' templates/free_place.html  templates/edit_stay.html

sed -i 's/Zwolnij miejsce/Release the berth/g' templates/add_leave.html 
sed -i 's/Data Do/Date to/g' templates/free_place.html

sed -i 's/Kontakt:/Contact/g' templates/resident_place.html  templates/free_place.html

sed -i 's/telefon:/phone/g'  templates/resident_place.html

sed -i 's/email:/email/g'  templates/resident_place.html

sed -i 's/Usuń/Delete/g'  templates/resident_place.html

sed -i 's/Długość:/Length/g' templates/chart_ui.html

sed -i 's/Data Od:/Date From/g' templates/chart_ui.html

sed -i 's/Do:/To/g' templates/chart_ui.html

sed -i 's/Wolne/Free/g' templates/chart_ui.html

sed -i 's/Zajete/Occupied/g' templates/chart_ui.html

sed -i 's/Rezydenci/Residents/g' templates/chart_ui.html

sed -i 's/Postumenty/Service points/g' templates/chart_ui.html

sed -i 's/Y-Bomy/Y-Booms/g' templates/chart_ui.html

sed -i 's/Wybierz miejsce:/Choose your berth/g' templates/connect_counter.html

sed -i 's/Licznik:/Meter/g'  templates/hub.html

sed -i 's/Nazwa:/Name/g' templates/edit_place.html 
sed -i 's/Zamknij/Close/g' templates/place_state.html

sed -i 's/Długość minimalna/Minimum Length/g' templates/edit_place.html

sed -i 's/Długość maksymalna/Maximum Length/g' templates/edit_place.html

sed -i 's/Jacht/Boat/g' templates/free_place.html

sed -i 's/Długość/Length/g' templates/free_place.html

sed -i 's/wybierz flagę.../Choose a flag/g' templates/free_place.html

sed -i 's/Rodzaj postoju:/Type of layover/g' templates/free_place.html

sed -i 's/Postój/Layover/g' templates/free_place.html

sed -i 's/Rezydent/Resident/g' templates/free_place.html

sed -i 's/Telefon:/Phone/g' templates/free_place.html

sed -i 's/Email:/Email/g' templates/free_place.html

sed -i 's/Uwagi:/Comments/g' templates/free_place.html

sed -i 's/Dodaj postój/Add layover/g'  templates/place_state.html

sed -i 's/Podłącz jacht/Connect boat/g' templates/hub.html

sed -i 's/Zapisz liczniki/Save the meter status/g' templates/hub.html

sed -i 's/Miejsce postojowe/Berth/g' templates/place_state.html

sed -i 's/metrów/meters/g' templates/place_state.html

sed -i 's/Edytuj miejsce postojowe/Edit berth/g' templates/place_state.html

sed -i 's/Zapisz/Save/g' templates/place_state.html

sed -i 's/od/from/g' templates/resident_place.html

sed -i 's/do/to/g' templates/resident_place.html
