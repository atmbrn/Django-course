from django.http import HttpRequest, HttpResponse


def set_cookies(request: HttpRequest) -> HttpResponse:
    """
    Установити cookie в браузері.

    Django створює відповідь і за допомогою методу set_cookie()
    додає до неї cookie з назвою "test_value". Значенням ми зберігаємо
    рядкове представлення користувача (request.user).

    Cookie буде доступним у браузері доти, доки не мине термін дії
    (за замовчуванням – до закриття браузера або до дефолтного max-age).
    """
    response = HttpResponse("Cookies set!")
    response.set_cookie("test_key", str(request.user))
    return response


def get_cookies(request: HttpRequest) -> HttpResponse:
    """
    Прочитати cookie з назвою "test_value".

    Браузер автоматично надсилає cookie у заголовку COOKIE під час кожного запиту.
    Доступ до них здійснюється через request.COOKIES.
    """
    cookies = request.COOKIES.get("test_key")
    return HttpResponse(cookies)


def delete_cookies(_: HttpRequest) -> HttpResponse:
    """
    Видалити cookie "test_value".

    Django не може "стерти" cookie напряму — тому він відправляє cookie
    з тією ж назвою, але з датою, що вже минула. Браузер тоді сам видаляє її.
    """
    response = HttpResponse("Cookies deleted!")
    response.delete_cookie("test_key")
    return response


def set_session(request: HttpRequest) -> HttpResponse:
    """
    Зберегти значення у Django-сесію.

    Django зберігає дані сесії на сервері, а в браузер відправляє тільки
    sessionid — унікальний ключ доступу до цих даних.
    """
    request.session["color"] = "red"
    return HttpResponse("Color saved!")


def get_session(request: HttpRequest) -> HttpResponse:
    """
    Отримати значення зі сесії.

    Якщо ключа немає — повертаємо "unknown".
    """
    color = request.session.get("color", "unknown")
    return HttpResponse(f"Color is {color}")


def test_cookie_set(request: HttpRequest) -> HttpResponse:
    """
    Створити тестовий cookie.

    Django використовує set_test_cookie(), щоб перевірити,
    чи підтримує браузер cookie (особливо актуально на старих пристроях).
    """
    request.session.set_test_cookie()
    return HttpResponse("Test cookie set!")


def test_cookie_check(request: HttpRequest) -> HttpResponse:
    """
    Перевірити, чи браузер підтримує cookie.

    Якщо test_cookie_worked() повертає True — значить браузер надіслав cookie назад.
    Після перевірки тестове cookie обов'язково видаляється.
    """
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        return HttpResponse("Cookies supported! 👍")

    return HttpResponse("Cookies NOT supported ❌")


def update_session(request: HttpRequest) -> HttpResponse:
    """
    Оновити значення у сесії.

    Просте встановлення нового значення за ключем.
    Django сам зрозуміє, що сесія була змінена, і збереже її.
    """
    request.session["color"] = "blue"
    request.session["points"] = 100
    return HttpResponse("Updated!!")


def tricky_update(request: HttpRequest) -> HttpResponse:
    """
    Приклад 'підступного' оновлення.

    Якщо змінити вкладений об'єкт (наприклад словник) без перезапису,
    Django НЕ помітить зміну. Тому потрібно перезаписати ключ у сесії вручну.
    """
    data = request.session.get("cart", {})
    data["new_item"] = 123

    # Django НЕ зрозуміє, що cart змінився — треба вручну
    request.session["cart"] = data

    return HttpResponse("Fixed update!")


# python manage.py clearsessions - команда для видалення всіх протермінованих сесій
def clear_session(request: HttpRequest) -> HttpResponse:
    """
    Повністю очистити сесію.

    Метод flush():
    - видаляє всі дані сесії
    - створює нову порожню сесію
    - змінює sessionid

    Це щось типу "вийти з акаунта".
    """
    request.session.flush()
    return HttpResponse("Session cleared!")


def remove_key(request: HttpRequest) -> HttpResponse:
    """
    Видалити окремий ключ із сесії, якщо він є.

    pop(key, None) не викликає помилки, якщо ключ не існує.
    """
    request.session.pop("favorite_color", None)
    return HttpResponse("Color removed!")


def session_expire_date(request: HttpRequest) -> HttpResponse:
    """
    Показати, коли закінчиться сесія.

    Якщо не встановлено власний час життя (set_expiry),
    Django поверне час за замовчуванням: now() + SESSION_COOKIE_AGE.

    Особливість:
    - кожен доступ до сесії оновлює "момент модифікації"
    - тому час закінчення буде зміщуватись вперед при кожному запиті
    """
    # Потім можна подивитися, коли сесія закінчиться
    expire = request.session.get_expiry_date()
    return HttpResponse(f"Session will expire on: {expire}")


def custom_expire(request: HttpRequest) -> HttpResponse:
    """
    Встановити користувацький час життя сесії.

    У цьому випадку — 60 секунд (1 хвилина).
    Після виклику set_expiry() час закінчення буде фіксованим.
    """
    request.session["points"] = 42

    # Встановлюємо, щоб сесія жила 1 хвилину
    request.session.set_expiry(60)
    return HttpResponse("Session will expire in 1 minute!")


def expire_on_close(request: HttpRequest) -> HttpResponse:
    """
    Зробити так, щоб сесія зникала після закриття браузера.

    set_expiry(0) означає: не ставити дату expire,
    а використовувати "session cookie" — воно живе лише доки браузер відкритий.

    Працює не для всіх браузерів.
    """
    request.session["username"] = "Sergiy"

    # Сесія буде жити тільки поки браузер відкритий
    request.session.set_expiry(0)
    return HttpResponse("Session will expire when browser closes!")


def show_cookies(request: HttpRequest) -> HttpResponse:
    """
    Показати sessionid, який браузер надіслав на сервер.

    Це корисно як демонстрація того, що сесія працює через cookie.
    Якщо cookie sessionid немає — значить сесія не активна.
    """
    # Django зберігає session_id у кукі 'sessionid'
    session_cookie = request.COOKIES.get("sessionid", "No session cookie")
    return HttpResponse(f"Session cookie: {session_cookie}")


# ------------------ Visit counter views ------------------

def visit_counter(request: HttpRequest) -> HttpResponse:
    """
    Лічильник відвідувань:
    - безпечно читаємо значення через get()
    - якщо ключа немає, стартуємо з 0
    - збільшуємо на 1 і зберігаємо назад у сесію
    """
    count = request.session.get("visit_count", 0)
    count += 1
    request.session["visit_count"] = count
    return HttpResponse(f"You have visited this page {count} times")


def reset_visit_counter(request: HttpRequest) -> HttpResponse:
    """
    Скинути лічильник (видалити ключ з сесії) і перенаправити на сторінку лічильника.
    """
    request.session.pop("visit_count", None)
    from django.shortcuts import redirect

    return redirect("visit_counter")
