from dependency_injector import containers, providers

from utils.get_db import get_db


# Створюємо контейнер для залежностей
class Container(containers.DeclarativeContainer):
    # Створюємо провайдер для сесії
    session = providers.Resource(get_db)
