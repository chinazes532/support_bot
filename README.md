<h1>Feedback bot</h1>

<h1>Принцип работы</h1>

<p>Сообщения от пользователей копируются методом copyMessage в топик чата админа (админов). Новый топик создается сразу, как пользователь отправил вопрос. Один пользователь не может создать более одного топика.

Как переписку видит пользователь:</p> <br>

<img src="screenshots/what_user_sees.png" alt="Пример переписки" />

В свою очередь, администратор видит так: <br>

<img src="screenshots/what_admin_sees_1.png" alt="Пример переписки" />
<br>
<img src="screenshots/what_admin_sees_2.png" alt="Пример переписки" />
<br>

<h1>Установка</h1>

<h3>Системные требования</h3>

<ol>
    <li>Python 3.9 и выше.</li>
    <li>Колнируйте к себе репозиторий.</li>
    <li>Создайте виртуальное окружение.</li>
    <li>Замените нужные параметры в файле <code>config.py</code>.</li>
    <li>Установите зависимости <code>pip install -r requirements.txt</code>.</li>
    <li>Запустите файл <code>python3 main.py</code></li>
</ol>
