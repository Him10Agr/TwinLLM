from llm_engineering.domain.exceptions import ImproperlyConfigured

def split_user_name(user_name: str | None) -> tuple[str, str]:

    if user_name is None:
        raise ImproperlyConfigured("User name is empty")
    
    name = user_name.split(" ")
    if len(name) == 0:
        raise ImproperlyConfigured("User name is empty")
    elif len(name) == 1:
        first_name, last_name = name[0], name[0]
    else:
        first_name, last_name = " ".join(name[:-1]), name[-1]
    
    return first_name, last_name