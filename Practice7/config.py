def load_config():  # объявляется функ, хрвнит настройки подключения к бд в одном месте
    return{
        "host":"localhost", # где находится сервер (компьютер)
        "database":"postgres", # имя бд (postgres)
        "user":"postgres",
        "password":"1234"

    }