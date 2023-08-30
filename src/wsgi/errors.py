class ClientError(Exception):
    """ClientError with mm_user_id=%s. <###traceback###\n%s\n###traceback###>\n\n"""
    pass


class ProgrammerError(Exception):
    """ProgrammerError with mm_user_id=%s. <###traceback###\n%s\n###traceback###>\n\n"""
    pass
