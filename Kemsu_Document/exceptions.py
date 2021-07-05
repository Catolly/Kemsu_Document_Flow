class GroupNotFoundError(Exception):
    pass

class ThisUserIsAlreadyExistException(Exception):
    pass

class ThisEmailIsAlreadyExistError(Exception):
    pass

class DepartmentNotFoundException(Exception):
    pass

class UserWithThisFullNameDoesNotExistException(Exception):
    pass

class UserWithThisEmailDoesNotExistException(Exception):
    pass

class BypassSheetTemplateExistException(Exception):
    pass