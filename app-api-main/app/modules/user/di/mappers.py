from app.modules.user.mappers.user_mapper import UserMapper


def get_user_mapper() -> UserMapper:
    return UserMapper()
