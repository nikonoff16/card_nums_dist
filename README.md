# Утилита распределения номеров 
Эта утилита создается с одной целью - сделать получение номеров для медицинских карт в моей амбулаторной практике значительно проще. На данный момент ни одна из атоматизированных систем помощи врачу не удовлетворяет этому требоанию - приходится брать бумажку с номерами, выбирать его от туда, вычеркивать, и не потерять при этом несчастную бумажку (что происходит достаточно часто, к сожалению). 
Предполагается, что у нее будет два варианта: для командной строки (Windows, Unix) и Телеграм-бот. На данный момент есть рабочая CLI-утилита, которая по большей части неплохо справляется с поставленной задачей на конкретной рабочей станции. Для того, что чтобы масштабировать утилиту на мое отделение, чуть позднее будет создан уже упомянутый бот. Некоторые элементы подготовки к этому шагу уже сделаны - приложение умеет недопускать доступ к изменению файла с номерами, пока тот занят другим пользователем, умеет восстанавливать файл с номерами, если тот поврежден, а также сведены к минимуму ошибки, из-за которых может быть утеряна из оперативной памяти вся база свободных номеров. 
У CLI-утилиты есть несколько опций (чуть подробнее об их использовании будет рассказано позднее, когда будут добавлены еще некоторые возможности): 
- можно указать количество номеров, которое требуется получить;
- можно выбрать между последовательной выдачей номеров сначала или случайной выдачей (генератором псевднослучайных чисел). 
По умолчанию и без аргументов утилита выдает один номер, выбранный случайно. 

Задач еще масса: 
- научить скрипт находить свой абсолютный адрес (если добавить ее в Path, то файл с номерами утилита будет искать в директории, в которой она была запущена);
- сделать вывод номеров после создания списка (бывает любопытно посмотреть, все ли программа сделала правильно);
- научить программу видеть поврежденный файл (пока в силу способа работы с файлом это сделать нереально, но есть некоторые мысли по этому поводу). 
- таки переделать ее для работы в качестве бота (не такая уж мелкая задача).

Надеюсь, у меня все получится. 

