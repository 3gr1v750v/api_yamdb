def code_generator(username):
    """Генератор секретного кода для получения токена."""
    return username.encode("utf-8").hex()[:10]
