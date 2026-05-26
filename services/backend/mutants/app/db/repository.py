"""Repository layer for database operations."""

from datetime import date, datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import func, text
from sqlmodel import Session, select

from app.db.models import Category, Priority, Status, Task, TaskComment, TaskHistory, User
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


class UserRepository:
    """Repository for user database operations."""

    def __init__(self, session: Session) -> None:
        args = [session]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁUserRepositoryǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁUserRepositoryǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁUserRepositoryǁ__init____mutmut_orig(self, session: Session) -> None:
        self.session = session

    def xǁUserRepositoryǁ__init____mutmut_1(self, session: Session) -> None:
        self.session = None
    
    xǁUserRepositoryǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁUserRepositoryǁ__init____mutmut_1': xǁUserRepositoryǁ__init____mutmut_1
    }
    xǁUserRepositoryǁ__init____mutmut_orig.__name__ = 'xǁUserRepositoryǁ__init__'

    def create(self, user: User) -> User:
        args = [user]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁUserRepositoryǁcreate__mutmut_orig'), object.__getattribute__(self, 'xǁUserRepositoryǁcreate__mutmut_mutants'), args, kwargs, self)

    def xǁUserRepositoryǁcreate__mutmut_orig(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def xǁUserRepositoryǁcreate__mutmut_1(self, user: User) -> User:
        self.session.add(None)
        self.session.commit()
        self.session.refresh(user)
        return user

    def xǁUserRepositoryǁcreate__mutmut_2(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(None)
        return user
    
    xǁUserRepositoryǁcreate__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁUserRepositoryǁcreate__mutmut_1': xǁUserRepositoryǁcreate__mutmut_1, 
        'xǁUserRepositoryǁcreate__mutmut_2': xǁUserRepositoryǁcreate__mutmut_2
    }
    xǁUserRepositoryǁcreate__mutmut_orig.__name__ = 'xǁUserRepositoryǁcreate'

    def get_by_id(self, user_id: int) -> Optional[User]:
        args = [user_id]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁUserRepositoryǁget_by_id__mutmut_orig'), object.__getattribute__(self, 'xǁUserRepositoryǁget_by_id__mutmut_mutants'), args, kwargs, self)

    def xǁUserRepositoryǁget_by_id__mutmut_orig(self, user_id: int) -> Optional[User]:
        return self.session.get(User, user_id)

    def xǁUserRepositoryǁget_by_id__mutmut_1(self, user_id: int) -> Optional[User]:
        return self.session.get(None, user_id)

    def xǁUserRepositoryǁget_by_id__mutmut_2(self, user_id: int) -> Optional[User]:
        return self.session.get(User, None)

    def xǁUserRepositoryǁget_by_id__mutmut_3(self, user_id: int) -> Optional[User]:
        return self.session.get(user_id)

    def xǁUserRepositoryǁget_by_id__mutmut_4(self, user_id: int) -> Optional[User]:
        return self.session.get(User, )
    
    xǁUserRepositoryǁget_by_id__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁUserRepositoryǁget_by_id__mutmut_1': xǁUserRepositoryǁget_by_id__mutmut_1, 
        'xǁUserRepositoryǁget_by_id__mutmut_2': xǁUserRepositoryǁget_by_id__mutmut_2, 
        'xǁUserRepositoryǁget_by_id__mutmut_3': xǁUserRepositoryǁget_by_id__mutmut_3, 
        'xǁUserRepositoryǁget_by_id__mutmut_4': xǁUserRepositoryǁget_by_id__mutmut_4
    }
    xǁUserRepositoryǁget_by_id__mutmut_orig.__name__ = 'xǁUserRepositoryǁget_by_id'

    def get_by_email(self, email: str) -> Optional[User]:
        args = [email]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁUserRepositoryǁget_by_email__mutmut_orig'), object.__getattribute__(self, 'xǁUserRepositoryǁget_by_email__mutmut_mutants'), args, kwargs, self)

    def xǁUserRepositoryǁget_by_email__mutmut_orig(self, email: str) -> Optional[User]:
        return self.session.exec(select(User).where(User.email == email)).first()

    def xǁUserRepositoryǁget_by_email__mutmut_1(self, email: str) -> Optional[User]:
        return self.session.exec(None).first()

    def xǁUserRepositoryǁget_by_email__mutmut_2(self, email: str) -> Optional[User]:
        return self.session.exec(select(User).where(None)).first()

    def xǁUserRepositoryǁget_by_email__mutmut_3(self, email: str) -> Optional[User]:
        return self.session.exec(select(None).where(User.email == email)).first()

    def xǁUserRepositoryǁget_by_email__mutmut_4(self, email: str) -> Optional[User]:
        return self.session.exec(select(User).where(User.email != email)).first()
    
    xǁUserRepositoryǁget_by_email__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁUserRepositoryǁget_by_email__mutmut_1': xǁUserRepositoryǁget_by_email__mutmut_1, 
        'xǁUserRepositoryǁget_by_email__mutmut_2': xǁUserRepositoryǁget_by_email__mutmut_2, 
        'xǁUserRepositoryǁget_by_email__mutmut_3': xǁUserRepositoryǁget_by_email__mutmut_3, 
        'xǁUserRepositoryǁget_by_email__mutmut_4': xǁUserRepositoryǁget_by_email__mutmut_4
    }
    xǁUserRepositoryǁget_by_email__mutmut_orig.__name__ = 'xǁUserRepositoryǁget_by_email'


class CategoryRepository:
    """Repository for category database operations."""

    def __init__(self, session: Session) -> None:
        args = [session]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCategoryRepositoryǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁCategoryRepositoryǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁCategoryRepositoryǁ__init____mutmut_orig(self, session: Session) -> None:
        self.session = session

    def xǁCategoryRepositoryǁ__init____mutmut_1(self, session: Session) -> None:
        self.session = None
    
    xǁCategoryRepositoryǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCategoryRepositoryǁ__init____mutmut_1': xǁCategoryRepositoryǁ__init____mutmut_1
    }
    xǁCategoryRepositoryǁ__init____mutmut_orig.__name__ = 'xǁCategoryRepositoryǁ__init__'

    def create(self, category: Category) -> Category:
        args = [category]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCategoryRepositoryǁcreate__mutmut_orig'), object.__getattribute__(self, 'xǁCategoryRepositoryǁcreate__mutmut_mutants'), args, kwargs, self)

    def xǁCategoryRepositoryǁcreate__mutmut_orig(self, category: Category) -> Category:
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return category

    def xǁCategoryRepositoryǁcreate__mutmut_1(self, category: Category) -> Category:
        self.session.add(None)
        self.session.commit()
        self.session.refresh(category)
        return category

    def xǁCategoryRepositoryǁcreate__mutmut_2(self, category: Category) -> Category:
        self.session.add(category)
        self.session.commit()
        self.session.refresh(None)
        return category
    
    xǁCategoryRepositoryǁcreate__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCategoryRepositoryǁcreate__mutmut_1': xǁCategoryRepositoryǁcreate__mutmut_1, 
        'xǁCategoryRepositoryǁcreate__mutmut_2': xǁCategoryRepositoryǁcreate__mutmut_2
    }
    xǁCategoryRepositoryǁcreate__mutmut_orig.__name__ = 'xǁCategoryRepositoryǁcreate'

    def get_by_id(self, category_id: int) -> Optional[Category]:
        args = [category_id]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCategoryRepositoryǁget_by_id__mutmut_orig'), object.__getattribute__(self, 'xǁCategoryRepositoryǁget_by_id__mutmut_mutants'), args, kwargs, self)

    def xǁCategoryRepositoryǁget_by_id__mutmut_orig(self, category_id: int) -> Optional[Category]:
        return self.session.get(Category, category_id)

    def xǁCategoryRepositoryǁget_by_id__mutmut_1(self, category_id: int) -> Optional[Category]:
        return self.session.get(None, category_id)

    def xǁCategoryRepositoryǁget_by_id__mutmut_2(self, category_id: int) -> Optional[Category]:
        return self.session.get(Category, None)

    def xǁCategoryRepositoryǁget_by_id__mutmut_3(self, category_id: int) -> Optional[Category]:
        return self.session.get(category_id)

    def xǁCategoryRepositoryǁget_by_id__mutmut_4(self, category_id: int) -> Optional[Category]:
        return self.session.get(Category, )
    
    xǁCategoryRepositoryǁget_by_id__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCategoryRepositoryǁget_by_id__mutmut_1': xǁCategoryRepositoryǁget_by_id__mutmut_1, 
        'xǁCategoryRepositoryǁget_by_id__mutmut_2': xǁCategoryRepositoryǁget_by_id__mutmut_2, 
        'xǁCategoryRepositoryǁget_by_id__mutmut_3': xǁCategoryRepositoryǁget_by_id__mutmut_3, 
        'xǁCategoryRepositoryǁget_by_id__mutmut_4': xǁCategoryRepositoryǁget_by_id__mutmut_4
    }
    xǁCategoryRepositoryǁget_by_id__mutmut_orig.__name__ = 'xǁCategoryRepositoryǁget_by_id'

    def get_by_name(self, name: str) -> Optional[Category]:
        args = [name]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCategoryRepositoryǁget_by_name__mutmut_orig'), object.__getattribute__(self, 'xǁCategoryRepositoryǁget_by_name__mutmut_mutants'), args, kwargs, self)

    def xǁCategoryRepositoryǁget_by_name__mutmut_orig(self, name: str) -> Optional[Category]:
        return self.session.exec(select(Category).where(Category.name == name)).first()

    def xǁCategoryRepositoryǁget_by_name__mutmut_1(self, name: str) -> Optional[Category]:
        return self.session.exec(None).first()

    def xǁCategoryRepositoryǁget_by_name__mutmut_2(self, name: str) -> Optional[Category]:
        return self.session.exec(select(Category).where(None)).first()

    def xǁCategoryRepositoryǁget_by_name__mutmut_3(self, name: str) -> Optional[Category]:
        return self.session.exec(select(None).where(Category.name == name)).first()

    def xǁCategoryRepositoryǁget_by_name__mutmut_4(self, name: str) -> Optional[Category]:
        return self.session.exec(select(Category).where(Category.name != name)).first()
    
    xǁCategoryRepositoryǁget_by_name__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCategoryRepositoryǁget_by_name__mutmut_1': xǁCategoryRepositoryǁget_by_name__mutmut_1, 
        'xǁCategoryRepositoryǁget_by_name__mutmut_2': xǁCategoryRepositoryǁget_by_name__mutmut_2, 
        'xǁCategoryRepositoryǁget_by_name__mutmut_3': xǁCategoryRepositoryǁget_by_name__mutmut_3, 
        'xǁCategoryRepositoryǁget_by_name__mutmut_4': xǁCategoryRepositoryǁget_by_name__mutmut_4
    }
    xǁCategoryRepositoryǁget_by_name__mutmut_orig.__name__ = 'xǁCategoryRepositoryǁget_by_name'

    def delete_and_nullify_tasks(self, category_id: int) -> bool:
        args = [category_id]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_orig'), object.__getattribute__(self, 'xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_mutants'), args, kwargs, self)

    def xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_orig(self, category_id: int) -> bool:
        category = self.get_by_id(category_id)
        if not category:
            return False
        tasks = list(self.session.exec(select(Task).where(Task.category_id == category_id)).all())
        for task in tasks:
            task.category_id = None
            self.session.add(task)
        self.session.delete(category)
        self.session.commit()
        return True

    def xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_1(self, category_id: int) -> bool:
        category = None
        if not category:
            return False
        tasks = list(self.session.exec(select(Task).where(Task.category_id == category_id)).all())
        for task in tasks:
            task.category_id = None
            self.session.add(task)
        self.session.delete(category)
        self.session.commit()
        return True

    def xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_2(self, category_id: int) -> bool:
        category = self.get_by_id(None)
        if not category:
            return False
        tasks = list(self.session.exec(select(Task).where(Task.category_id == category_id)).all())
        for task in tasks:
            task.category_id = None
            self.session.add(task)
        self.session.delete(category)
        self.session.commit()
        return True

    def xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_3(self, category_id: int) -> bool:
        category = self.get_by_id(category_id)
        if category:
            return False
        tasks = list(self.session.exec(select(Task).where(Task.category_id == category_id)).all())
        for task in tasks:
            task.category_id = None
            self.session.add(task)
        self.session.delete(category)
        self.session.commit()
        return True

    def xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_4(self, category_id: int) -> bool:
        category = self.get_by_id(category_id)
        if not category:
            return True
        tasks = list(self.session.exec(select(Task).where(Task.category_id == category_id)).all())
        for task in tasks:
            task.category_id = None
            self.session.add(task)
        self.session.delete(category)
        self.session.commit()
        return True

    def xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_5(self, category_id: int) -> bool:
        category = self.get_by_id(category_id)
        if not category:
            return False
        tasks = None
        for task in tasks:
            task.category_id = None
            self.session.add(task)
        self.session.delete(category)
        self.session.commit()
        return True

    def xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_6(self, category_id: int) -> bool:
        category = self.get_by_id(category_id)
        if not category:
            return False
        tasks = list(None)
        for task in tasks:
            task.category_id = None
            self.session.add(task)
        self.session.delete(category)
        self.session.commit()
        return True

    def xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_7(self, category_id: int) -> bool:
        category = self.get_by_id(category_id)
        if not category:
            return False
        tasks = list(self.session.exec(None).all())
        for task in tasks:
            task.category_id = None
            self.session.add(task)
        self.session.delete(category)
        self.session.commit()
        return True

    def xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_8(self, category_id: int) -> bool:
        category = self.get_by_id(category_id)
        if not category:
            return False
        tasks = list(self.session.exec(select(Task).where(None)).all())
        for task in tasks:
            task.category_id = None
            self.session.add(task)
        self.session.delete(category)
        self.session.commit()
        return True

    def xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_9(self, category_id: int) -> bool:
        category = self.get_by_id(category_id)
        if not category:
            return False
        tasks = list(self.session.exec(select(None).where(Task.category_id == category_id)).all())
        for task in tasks:
            task.category_id = None
            self.session.add(task)
        self.session.delete(category)
        self.session.commit()
        return True

    def xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_10(self, category_id: int) -> bool:
        category = self.get_by_id(category_id)
        if not category:
            return False
        tasks = list(self.session.exec(select(Task).where(Task.category_id != category_id)).all())
        for task in tasks:
            task.category_id = None
            self.session.add(task)
        self.session.delete(category)
        self.session.commit()
        return True

    def xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_11(self, category_id: int) -> bool:
        category = self.get_by_id(category_id)
        if not category:
            return False
        tasks = list(self.session.exec(select(Task).where(Task.category_id == category_id)).all())
        for task in tasks:
            task.category_id = ""
            self.session.add(task)
        self.session.delete(category)
        self.session.commit()
        return True

    def xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_12(self, category_id: int) -> bool:
        category = self.get_by_id(category_id)
        if not category:
            return False
        tasks = list(self.session.exec(select(Task).where(Task.category_id == category_id)).all())
        for task in tasks:
            task.category_id = None
            self.session.add(None)
        self.session.delete(category)
        self.session.commit()
        return True

    def xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_13(self, category_id: int) -> bool:
        category = self.get_by_id(category_id)
        if not category:
            return False
        tasks = list(self.session.exec(select(Task).where(Task.category_id == category_id)).all())
        for task in tasks:
            task.category_id = None
            self.session.add(task)
        self.session.delete(None)
        self.session.commit()
        return True

    def xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_14(self, category_id: int) -> bool:
        category = self.get_by_id(category_id)
        if not category:
            return False
        tasks = list(self.session.exec(select(Task).where(Task.category_id == category_id)).all())
        for task in tasks:
            task.category_id = None
            self.session.add(task)
        self.session.delete(category)
        self.session.commit()
        return False
    
    xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_1': xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_1, 
        'xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_2': xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_2, 
        'xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_3': xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_3, 
        'xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_4': xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_4, 
        'xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_5': xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_5, 
        'xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_6': xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_6, 
        'xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_7': xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_7, 
        'xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_8': xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_8, 
        'xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_9': xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_9, 
        'xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_10': xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_10, 
        'xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_11': xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_11, 
        'xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_12': xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_12, 
        'xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_13': xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_13, 
        'xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_14': xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_14
    }
    xǁCategoryRepositoryǁdelete_and_nullify_tasks__mutmut_orig.__name__ = 'xǁCategoryRepositoryǁdelete_and_nullify_tasks'


class TaskRepository:
    """Repository for task database operations."""

    def __init__(self, session: Session) -> None:
        args = [session]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskRepositoryǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁTaskRepositoryǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁTaskRepositoryǁ__init____mutmut_orig(self, session: Session) -> None:
        """Initialize repository with database session."""
        self.session = session

    def xǁTaskRepositoryǁ__init____mutmut_1(self, session: Session) -> None:
        """Initialize repository with database session."""
        self.session = None
    
    xǁTaskRepositoryǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskRepositoryǁ__init____mutmut_1': xǁTaskRepositoryǁ__init____mutmut_1
    }
    xǁTaskRepositoryǁ__init____mutmut_orig.__name__ = 'xǁTaskRepositoryǁ__init__'

    def create(self, task: Task) -> Task:
        args = [task]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskRepositoryǁcreate__mutmut_orig'), object.__getattribute__(self, 'xǁTaskRepositoryǁcreate__mutmut_mutants'), args, kwargs, self)

    def xǁTaskRepositoryǁcreate__mutmut_orig(self, task: Task) -> Task:
        """Create a new task."""
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def xǁTaskRepositoryǁcreate__mutmut_1(self, task: Task) -> Task:
        """Create a new task."""
        self.session.add(None)
        self.session.commit()
        self.session.refresh(task)
        return task

    def xǁTaskRepositoryǁcreate__mutmut_2(self, task: Task) -> Task:
        """Create a new task."""
        self.session.add(task)
        self.session.commit()
        self.session.refresh(None)
        return task
    
    xǁTaskRepositoryǁcreate__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskRepositoryǁcreate__mutmut_1': xǁTaskRepositoryǁcreate__mutmut_1, 
        'xǁTaskRepositoryǁcreate__mutmut_2': xǁTaskRepositoryǁcreate__mutmut_2
    }
    xǁTaskRepositoryǁcreate__mutmut_orig.__name__ = 'xǁTaskRepositoryǁcreate'

    def get_by_id(self, task_id: int, owner_id: Optional[int] = None) -> Optional[Task]:
        args = [task_id, owner_id]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskRepositoryǁget_by_id__mutmut_orig'), object.__getattribute__(self, 'xǁTaskRepositoryǁget_by_id__mutmut_mutants'), args, kwargs, self)

    def xǁTaskRepositoryǁget_by_id__mutmut_orig(self, task_id: int, owner_id: Optional[int] = None) -> Optional[Task]:
        """Get a task by ID, optionally scoped to an owner."""
        task = self.session.get(Task, task_id)
        if task is None:
            return None
        if owner_id is not None and task.owner_id != owner_id:
            return None
        return task

    def xǁTaskRepositoryǁget_by_id__mutmut_1(self, task_id: int, owner_id: Optional[int] = None) -> Optional[Task]:
        """Get a task by ID, optionally scoped to an owner."""
        task = None
        if task is None:
            return None
        if owner_id is not None and task.owner_id != owner_id:
            return None
        return task

    def xǁTaskRepositoryǁget_by_id__mutmut_2(self, task_id: int, owner_id: Optional[int] = None) -> Optional[Task]:
        """Get a task by ID, optionally scoped to an owner."""
        task = self.session.get(None, task_id)
        if task is None:
            return None
        if owner_id is not None and task.owner_id != owner_id:
            return None
        return task

    def xǁTaskRepositoryǁget_by_id__mutmut_3(self, task_id: int, owner_id: Optional[int] = None) -> Optional[Task]:
        """Get a task by ID, optionally scoped to an owner."""
        task = self.session.get(Task, None)
        if task is None:
            return None
        if owner_id is not None and task.owner_id != owner_id:
            return None
        return task

    def xǁTaskRepositoryǁget_by_id__mutmut_4(self, task_id: int, owner_id: Optional[int] = None) -> Optional[Task]:
        """Get a task by ID, optionally scoped to an owner."""
        task = self.session.get(task_id)
        if task is None:
            return None
        if owner_id is not None and task.owner_id != owner_id:
            return None
        return task

    def xǁTaskRepositoryǁget_by_id__mutmut_5(self, task_id: int, owner_id: Optional[int] = None) -> Optional[Task]:
        """Get a task by ID, optionally scoped to an owner."""
        task = self.session.get(Task, )
        if task is None:
            return None
        if owner_id is not None and task.owner_id != owner_id:
            return None
        return task

    def xǁTaskRepositoryǁget_by_id__mutmut_6(self, task_id: int, owner_id: Optional[int] = None) -> Optional[Task]:
        """Get a task by ID, optionally scoped to an owner."""
        task = self.session.get(Task, task_id)
        if task is not None:
            return None
        if owner_id is not None and task.owner_id != owner_id:
            return None
        return task

    def xǁTaskRepositoryǁget_by_id__mutmut_7(self, task_id: int, owner_id: Optional[int] = None) -> Optional[Task]:
        """Get a task by ID, optionally scoped to an owner."""
        task = self.session.get(Task, task_id)
        if task is None:
            return None
        if owner_id is not None or task.owner_id != owner_id:
            return None
        return task

    def xǁTaskRepositoryǁget_by_id__mutmut_8(self, task_id: int, owner_id: Optional[int] = None) -> Optional[Task]:
        """Get a task by ID, optionally scoped to an owner."""
        task = self.session.get(Task, task_id)
        if task is None:
            return None
        if owner_id is None and task.owner_id != owner_id:
            return None
        return task

    def xǁTaskRepositoryǁget_by_id__mutmut_9(self, task_id: int, owner_id: Optional[int] = None) -> Optional[Task]:
        """Get a task by ID, optionally scoped to an owner."""
        task = self.session.get(Task, task_id)
        if task is None:
            return None
        if owner_id is not None and task.owner_id == owner_id:
            return None
        return task
    
    xǁTaskRepositoryǁget_by_id__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskRepositoryǁget_by_id__mutmut_1': xǁTaskRepositoryǁget_by_id__mutmut_1, 
        'xǁTaskRepositoryǁget_by_id__mutmut_2': xǁTaskRepositoryǁget_by_id__mutmut_2, 
        'xǁTaskRepositoryǁget_by_id__mutmut_3': xǁTaskRepositoryǁget_by_id__mutmut_3, 
        'xǁTaskRepositoryǁget_by_id__mutmut_4': xǁTaskRepositoryǁget_by_id__mutmut_4, 
        'xǁTaskRepositoryǁget_by_id__mutmut_5': xǁTaskRepositoryǁget_by_id__mutmut_5, 
        'xǁTaskRepositoryǁget_by_id__mutmut_6': xǁTaskRepositoryǁget_by_id__mutmut_6, 
        'xǁTaskRepositoryǁget_by_id__mutmut_7': xǁTaskRepositoryǁget_by_id__mutmut_7, 
        'xǁTaskRepositoryǁget_by_id__mutmut_8': xǁTaskRepositoryǁget_by_id__mutmut_8, 
        'xǁTaskRepositoryǁget_by_id__mutmut_9': xǁTaskRepositoryǁget_by_id__mutmut_9
    }
    xǁTaskRepositoryǁget_by_id__mutmut_orig.__name__ = 'xǁTaskRepositoryǁget_by_id'

    def get_category(self, category_id: int) -> Optional[Category]:
        args = [category_id]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskRepositoryǁget_category__mutmut_orig'), object.__getattribute__(self, 'xǁTaskRepositoryǁget_category__mutmut_mutants'), args, kwargs, self)

    def xǁTaskRepositoryǁget_category__mutmut_orig(self, category_id: int) -> Optional[Category]:
        """Get a category by ID."""
        return self.session.get(Category, category_id)

    def xǁTaskRepositoryǁget_category__mutmut_1(self, category_id: int) -> Optional[Category]:
        """Get a category by ID."""
        return self.session.get(None, category_id)

    def xǁTaskRepositoryǁget_category__mutmut_2(self, category_id: int) -> Optional[Category]:
        """Get a category by ID."""
        return self.session.get(Category, None)

    def xǁTaskRepositoryǁget_category__mutmut_3(self, category_id: int) -> Optional[Category]:
        """Get a category by ID."""
        return self.session.get(category_id)

    def xǁTaskRepositoryǁget_category__mutmut_4(self, category_id: int) -> Optional[Category]:
        """Get a category by ID."""
        return self.session.get(Category, )
    
    xǁTaskRepositoryǁget_category__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskRepositoryǁget_category__mutmut_1': xǁTaskRepositoryǁget_category__mutmut_1, 
        'xǁTaskRepositoryǁget_category__mutmut_2': xǁTaskRepositoryǁget_category__mutmut_2, 
        'xǁTaskRepositoryǁget_category__mutmut_3': xǁTaskRepositoryǁget_category__mutmut_3, 
        'xǁTaskRepositoryǁget_category__mutmut_4': xǁTaskRepositoryǁget_category__mutmut_4
    }
    xǁTaskRepositoryǁget_category__mutmut_orig.__name__ = 'xǁTaskRepositoryǁget_category'

    def get_all(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        args = [status, priority, skip, limit, owner_id, category_id, tag, overdue]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskRepositoryǁget_all__mutmut_orig'), object.__getattribute__(self, 'xǁTaskRepositoryǁget_all__mutmut_mutants'), args, kwargs, self)

    def xǁTaskRepositoryǁget_all__mutmut_orig(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_1(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 1,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_2(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 101,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_3(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = True,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_4(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = None

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_5(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(None)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_6(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_7(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = None
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_8(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(None)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_9(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id != owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_10(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = None
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_11(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(None)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_12(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status != status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_13(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = None
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_14(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(None)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_15(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority != priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_16(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_17(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = None
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_18(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(None)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_19(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id != category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_20(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_21(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = None
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_22(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                None
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_23(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=None)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_24(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    None
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_25(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "XXEXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)XX"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_26(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "exists (select 1 from json_each(task.tags) where value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_27(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM JSON_EACH(TASK.TAGS) WHERE VALUE = :TAG_VAL)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_28(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = None
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_29(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = None

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_30(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(None)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_31(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(None).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_32(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date <= today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_33(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status == Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_34(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = None
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_35(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(None)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_36(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(None).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_all__mutmut_37(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(None)

    def xǁTaskRepositoryǁget_all__mutmut_38(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """Get all tasks with optional filtering."""
        statement = select(Task)

        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category_id is not None:
            statement = statement.where(Task.category_id == category_id)
        if tag is not None:
            statement = statement.where(
                text(
                    "EXISTS (SELECT 1 FROM json_each(task.tags) WHERE value = :tag_val)"
                ).bindparams(tag_val=tag)
            )
        if overdue:
            today = date.today()
            statement = statement.where(Task.due_date < today).where(Task.status != Status.DONE)

        statement = statement.offset(skip).limit(limit)
        return list(self.session.exec(None).all())
    
    xǁTaskRepositoryǁget_all__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskRepositoryǁget_all__mutmut_1': xǁTaskRepositoryǁget_all__mutmut_1, 
        'xǁTaskRepositoryǁget_all__mutmut_2': xǁTaskRepositoryǁget_all__mutmut_2, 
        'xǁTaskRepositoryǁget_all__mutmut_3': xǁTaskRepositoryǁget_all__mutmut_3, 
        'xǁTaskRepositoryǁget_all__mutmut_4': xǁTaskRepositoryǁget_all__mutmut_4, 
        'xǁTaskRepositoryǁget_all__mutmut_5': xǁTaskRepositoryǁget_all__mutmut_5, 
        'xǁTaskRepositoryǁget_all__mutmut_6': xǁTaskRepositoryǁget_all__mutmut_6, 
        'xǁTaskRepositoryǁget_all__mutmut_7': xǁTaskRepositoryǁget_all__mutmut_7, 
        'xǁTaskRepositoryǁget_all__mutmut_8': xǁTaskRepositoryǁget_all__mutmut_8, 
        'xǁTaskRepositoryǁget_all__mutmut_9': xǁTaskRepositoryǁget_all__mutmut_9, 
        'xǁTaskRepositoryǁget_all__mutmut_10': xǁTaskRepositoryǁget_all__mutmut_10, 
        'xǁTaskRepositoryǁget_all__mutmut_11': xǁTaskRepositoryǁget_all__mutmut_11, 
        'xǁTaskRepositoryǁget_all__mutmut_12': xǁTaskRepositoryǁget_all__mutmut_12, 
        'xǁTaskRepositoryǁget_all__mutmut_13': xǁTaskRepositoryǁget_all__mutmut_13, 
        'xǁTaskRepositoryǁget_all__mutmut_14': xǁTaskRepositoryǁget_all__mutmut_14, 
        'xǁTaskRepositoryǁget_all__mutmut_15': xǁTaskRepositoryǁget_all__mutmut_15, 
        'xǁTaskRepositoryǁget_all__mutmut_16': xǁTaskRepositoryǁget_all__mutmut_16, 
        'xǁTaskRepositoryǁget_all__mutmut_17': xǁTaskRepositoryǁget_all__mutmut_17, 
        'xǁTaskRepositoryǁget_all__mutmut_18': xǁTaskRepositoryǁget_all__mutmut_18, 
        'xǁTaskRepositoryǁget_all__mutmut_19': xǁTaskRepositoryǁget_all__mutmut_19, 
        'xǁTaskRepositoryǁget_all__mutmut_20': xǁTaskRepositoryǁget_all__mutmut_20, 
        'xǁTaskRepositoryǁget_all__mutmut_21': xǁTaskRepositoryǁget_all__mutmut_21, 
        'xǁTaskRepositoryǁget_all__mutmut_22': xǁTaskRepositoryǁget_all__mutmut_22, 
        'xǁTaskRepositoryǁget_all__mutmut_23': xǁTaskRepositoryǁget_all__mutmut_23, 
        'xǁTaskRepositoryǁget_all__mutmut_24': xǁTaskRepositoryǁget_all__mutmut_24, 
        'xǁTaskRepositoryǁget_all__mutmut_25': xǁTaskRepositoryǁget_all__mutmut_25, 
        'xǁTaskRepositoryǁget_all__mutmut_26': xǁTaskRepositoryǁget_all__mutmut_26, 
        'xǁTaskRepositoryǁget_all__mutmut_27': xǁTaskRepositoryǁget_all__mutmut_27, 
        'xǁTaskRepositoryǁget_all__mutmut_28': xǁTaskRepositoryǁget_all__mutmut_28, 
        'xǁTaskRepositoryǁget_all__mutmut_29': xǁTaskRepositoryǁget_all__mutmut_29, 
        'xǁTaskRepositoryǁget_all__mutmut_30': xǁTaskRepositoryǁget_all__mutmut_30, 
        'xǁTaskRepositoryǁget_all__mutmut_31': xǁTaskRepositoryǁget_all__mutmut_31, 
        'xǁTaskRepositoryǁget_all__mutmut_32': xǁTaskRepositoryǁget_all__mutmut_32, 
        'xǁTaskRepositoryǁget_all__mutmut_33': xǁTaskRepositoryǁget_all__mutmut_33, 
        'xǁTaskRepositoryǁget_all__mutmut_34': xǁTaskRepositoryǁget_all__mutmut_34, 
        'xǁTaskRepositoryǁget_all__mutmut_35': xǁTaskRepositoryǁget_all__mutmut_35, 
        'xǁTaskRepositoryǁget_all__mutmut_36': xǁTaskRepositoryǁget_all__mutmut_36, 
        'xǁTaskRepositoryǁget_all__mutmut_37': xǁTaskRepositoryǁget_all__mutmut_37, 
        'xǁTaskRepositoryǁget_all__mutmut_38': xǁTaskRepositoryǁget_all__mutmut_38
    }
    xǁTaskRepositoryǁget_all__mutmut_orig.__name__ = 'xǁTaskRepositoryǁget_all'

    def get_upcoming(
        self,
        days: int,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        args = [days, owner_id, skip, limit]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskRepositoryǁget_upcoming__mutmut_orig'), object.__getattribute__(self, 'xǁTaskRepositoryǁget_upcoming__mutmut_mutants'), args, kwargs, self)

    def xǁTaskRepositoryǁget_upcoming__mutmut_orig(
        self,
        days: int,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """Get tasks due within the next `days` days (not yet done)."""
        today = date.today()
        cutoff = today + timedelta(days=days)
        statement = (
            select(Task)
            .where(Task.due_date >= today)
            .where(Task.due_date <= cutoff)
            .where(Task.status != Status.DONE)
        )
        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        statement = statement.order_by(Task.due_date).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_upcoming__mutmut_1(
        self,
        days: int,
        owner_id: Optional[int] = None,
        skip: int = 1,
        limit: int = 100,
    ) -> list[Task]:
        """Get tasks due within the next `days` days (not yet done)."""
        today = date.today()
        cutoff = today + timedelta(days=days)
        statement = (
            select(Task)
            .where(Task.due_date >= today)
            .where(Task.due_date <= cutoff)
            .where(Task.status != Status.DONE)
        )
        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        statement = statement.order_by(Task.due_date).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_upcoming__mutmut_2(
        self,
        days: int,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 101,
    ) -> list[Task]:
        """Get tasks due within the next `days` days (not yet done)."""
        today = date.today()
        cutoff = today + timedelta(days=days)
        statement = (
            select(Task)
            .where(Task.due_date >= today)
            .where(Task.due_date <= cutoff)
            .where(Task.status != Status.DONE)
        )
        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        statement = statement.order_by(Task.due_date).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_upcoming__mutmut_3(
        self,
        days: int,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """Get tasks due within the next `days` days (not yet done)."""
        today = None
        cutoff = today + timedelta(days=days)
        statement = (
            select(Task)
            .where(Task.due_date >= today)
            .where(Task.due_date <= cutoff)
            .where(Task.status != Status.DONE)
        )
        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        statement = statement.order_by(Task.due_date).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_upcoming__mutmut_4(
        self,
        days: int,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """Get tasks due within the next `days` days (not yet done)."""
        today = date.today()
        cutoff = None
        statement = (
            select(Task)
            .where(Task.due_date >= today)
            .where(Task.due_date <= cutoff)
            .where(Task.status != Status.DONE)
        )
        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        statement = statement.order_by(Task.due_date).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_upcoming__mutmut_5(
        self,
        days: int,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """Get tasks due within the next `days` days (not yet done)."""
        today = date.today()
        cutoff = today - timedelta(days=days)
        statement = (
            select(Task)
            .where(Task.due_date >= today)
            .where(Task.due_date <= cutoff)
            .where(Task.status != Status.DONE)
        )
        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        statement = statement.order_by(Task.due_date).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_upcoming__mutmut_6(
        self,
        days: int,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """Get tasks due within the next `days` days (not yet done)."""
        today = date.today()
        cutoff = today + timedelta(days=None)
        statement = (
            select(Task)
            .where(Task.due_date >= today)
            .where(Task.due_date <= cutoff)
            .where(Task.status != Status.DONE)
        )
        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        statement = statement.order_by(Task.due_date).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_upcoming__mutmut_7(
        self,
        days: int,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """Get tasks due within the next `days` days (not yet done)."""
        today = date.today()
        cutoff = today + timedelta(days=days)
        statement = None
        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        statement = statement.order_by(Task.due_date).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_upcoming__mutmut_8(
        self,
        days: int,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """Get tasks due within the next `days` days (not yet done)."""
        today = date.today()
        cutoff = today + timedelta(days=days)
        statement = (
            select(Task)
            .where(Task.due_date >= today)
            .where(Task.due_date <= cutoff)
            .where(None)
        )
        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        statement = statement.order_by(Task.due_date).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_upcoming__mutmut_9(
        self,
        days: int,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """Get tasks due within the next `days` days (not yet done)."""
        today = date.today()
        cutoff = today + timedelta(days=days)
        statement = (
            select(Task)
            .where(Task.due_date >= today)
            .where(None)
            .where(Task.status != Status.DONE)
        )
        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        statement = statement.order_by(Task.due_date).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_upcoming__mutmut_10(
        self,
        days: int,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """Get tasks due within the next `days` days (not yet done)."""
        today = date.today()
        cutoff = today + timedelta(days=days)
        statement = (
            select(Task)
            .where(None)
            .where(Task.due_date <= cutoff)
            .where(Task.status != Status.DONE)
        )
        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        statement = statement.order_by(Task.due_date).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_upcoming__mutmut_11(
        self,
        days: int,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """Get tasks due within the next `days` days (not yet done)."""
        today = date.today()
        cutoff = today + timedelta(days=days)
        statement = (
            select(None)
            .where(Task.due_date >= today)
            .where(Task.due_date <= cutoff)
            .where(Task.status != Status.DONE)
        )
        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        statement = statement.order_by(Task.due_date).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_upcoming__mutmut_12(
        self,
        days: int,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """Get tasks due within the next `days` days (not yet done)."""
        today = date.today()
        cutoff = today + timedelta(days=days)
        statement = (
            select(Task)
            .where(Task.due_date > today)
            .where(Task.due_date <= cutoff)
            .where(Task.status != Status.DONE)
        )
        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        statement = statement.order_by(Task.due_date).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_upcoming__mutmut_13(
        self,
        days: int,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """Get tasks due within the next `days` days (not yet done)."""
        today = date.today()
        cutoff = today + timedelta(days=days)
        statement = (
            select(Task)
            .where(Task.due_date >= today)
            .where(Task.due_date < cutoff)
            .where(Task.status != Status.DONE)
        )
        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        statement = statement.order_by(Task.due_date).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_upcoming__mutmut_14(
        self,
        days: int,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """Get tasks due within the next `days` days (not yet done)."""
        today = date.today()
        cutoff = today + timedelta(days=days)
        statement = (
            select(Task)
            .where(Task.due_date >= today)
            .where(Task.due_date <= cutoff)
            .where(Task.status == Status.DONE)
        )
        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        statement = statement.order_by(Task.due_date).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_upcoming__mutmut_15(
        self,
        days: int,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """Get tasks due within the next `days` days (not yet done)."""
        today = date.today()
        cutoff = today + timedelta(days=days)
        statement = (
            select(Task)
            .where(Task.due_date >= today)
            .where(Task.due_date <= cutoff)
            .where(Task.status != Status.DONE)
        )
        if owner_id is None:
            statement = statement.where(Task.owner_id == owner_id)
        statement = statement.order_by(Task.due_date).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_upcoming__mutmut_16(
        self,
        days: int,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """Get tasks due within the next `days` days (not yet done)."""
        today = date.today()
        cutoff = today + timedelta(days=days)
        statement = (
            select(Task)
            .where(Task.due_date >= today)
            .where(Task.due_date <= cutoff)
            .where(Task.status != Status.DONE)
        )
        if owner_id is not None:
            statement = None
        statement = statement.order_by(Task.due_date).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_upcoming__mutmut_17(
        self,
        days: int,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """Get tasks due within the next `days` days (not yet done)."""
        today = date.today()
        cutoff = today + timedelta(days=days)
        statement = (
            select(Task)
            .where(Task.due_date >= today)
            .where(Task.due_date <= cutoff)
            .where(Task.status != Status.DONE)
        )
        if owner_id is not None:
            statement = statement.where(None)
        statement = statement.order_by(Task.due_date).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_upcoming__mutmut_18(
        self,
        days: int,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """Get tasks due within the next `days` days (not yet done)."""
        today = date.today()
        cutoff = today + timedelta(days=days)
        statement = (
            select(Task)
            .where(Task.due_date >= today)
            .where(Task.due_date <= cutoff)
            .where(Task.status != Status.DONE)
        )
        if owner_id is not None:
            statement = statement.where(Task.owner_id != owner_id)
        statement = statement.order_by(Task.due_date).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_upcoming__mutmut_19(
        self,
        days: int,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """Get tasks due within the next `days` days (not yet done)."""
        today = date.today()
        cutoff = today + timedelta(days=days)
        statement = (
            select(Task)
            .where(Task.due_date >= today)
            .where(Task.due_date <= cutoff)
            .where(Task.status != Status.DONE)
        )
        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        statement = None
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_upcoming__mutmut_20(
        self,
        days: int,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """Get tasks due within the next `days` days (not yet done)."""
        today = date.today()
        cutoff = today + timedelta(days=days)
        statement = (
            select(Task)
            .where(Task.due_date >= today)
            .where(Task.due_date <= cutoff)
            .where(Task.status != Status.DONE)
        )
        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        statement = statement.order_by(Task.due_date).offset(skip).limit(None)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_upcoming__mutmut_21(
        self,
        days: int,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """Get tasks due within the next `days` days (not yet done)."""
        today = date.today()
        cutoff = today + timedelta(days=days)
        statement = (
            select(Task)
            .where(Task.due_date >= today)
            .where(Task.due_date <= cutoff)
            .where(Task.status != Status.DONE)
        )
        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        statement = statement.order_by(Task.due_date).offset(None).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_upcoming__mutmut_22(
        self,
        days: int,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """Get tasks due within the next `days` days (not yet done)."""
        today = date.today()
        cutoff = today + timedelta(days=days)
        statement = (
            select(Task)
            .where(Task.due_date >= today)
            .where(Task.due_date <= cutoff)
            .where(Task.status != Status.DONE)
        )
        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        statement = statement.order_by(None).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def xǁTaskRepositoryǁget_upcoming__mutmut_23(
        self,
        days: int,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """Get tasks due within the next `days` days (not yet done)."""
        today = date.today()
        cutoff = today + timedelta(days=days)
        statement = (
            select(Task)
            .where(Task.due_date >= today)
            .where(Task.due_date <= cutoff)
            .where(Task.status != Status.DONE)
        )
        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        statement = statement.order_by(Task.due_date).offset(skip).limit(limit)
        return list(None)

    def xǁTaskRepositoryǁget_upcoming__mutmut_24(
        self,
        days: int,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """Get tasks due within the next `days` days (not yet done)."""
        today = date.today()
        cutoff = today + timedelta(days=days)
        statement = (
            select(Task)
            .where(Task.due_date >= today)
            .where(Task.due_date <= cutoff)
            .where(Task.status != Status.DONE)
        )
        if owner_id is not None:
            statement = statement.where(Task.owner_id == owner_id)
        statement = statement.order_by(Task.due_date).offset(skip).limit(limit)
        return list(self.session.exec(None).all())
    
    xǁTaskRepositoryǁget_upcoming__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskRepositoryǁget_upcoming__mutmut_1': xǁTaskRepositoryǁget_upcoming__mutmut_1, 
        'xǁTaskRepositoryǁget_upcoming__mutmut_2': xǁTaskRepositoryǁget_upcoming__mutmut_2, 
        'xǁTaskRepositoryǁget_upcoming__mutmut_3': xǁTaskRepositoryǁget_upcoming__mutmut_3, 
        'xǁTaskRepositoryǁget_upcoming__mutmut_4': xǁTaskRepositoryǁget_upcoming__mutmut_4, 
        'xǁTaskRepositoryǁget_upcoming__mutmut_5': xǁTaskRepositoryǁget_upcoming__mutmut_5, 
        'xǁTaskRepositoryǁget_upcoming__mutmut_6': xǁTaskRepositoryǁget_upcoming__mutmut_6, 
        'xǁTaskRepositoryǁget_upcoming__mutmut_7': xǁTaskRepositoryǁget_upcoming__mutmut_7, 
        'xǁTaskRepositoryǁget_upcoming__mutmut_8': xǁTaskRepositoryǁget_upcoming__mutmut_8, 
        'xǁTaskRepositoryǁget_upcoming__mutmut_9': xǁTaskRepositoryǁget_upcoming__mutmut_9, 
        'xǁTaskRepositoryǁget_upcoming__mutmut_10': xǁTaskRepositoryǁget_upcoming__mutmut_10, 
        'xǁTaskRepositoryǁget_upcoming__mutmut_11': xǁTaskRepositoryǁget_upcoming__mutmut_11, 
        'xǁTaskRepositoryǁget_upcoming__mutmut_12': xǁTaskRepositoryǁget_upcoming__mutmut_12, 
        'xǁTaskRepositoryǁget_upcoming__mutmut_13': xǁTaskRepositoryǁget_upcoming__mutmut_13, 
        'xǁTaskRepositoryǁget_upcoming__mutmut_14': xǁTaskRepositoryǁget_upcoming__mutmut_14, 
        'xǁTaskRepositoryǁget_upcoming__mutmut_15': xǁTaskRepositoryǁget_upcoming__mutmut_15, 
        'xǁTaskRepositoryǁget_upcoming__mutmut_16': xǁTaskRepositoryǁget_upcoming__mutmut_16, 
        'xǁTaskRepositoryǁget_upcoming__mutmut_17': xǁTaskRepositoryǁget_upcoming__mutmut_17, 
        'xǁTaskRepositoryǁget_upcoming__mutmut_18': xǁTaskRepositoryǁget_upcoming__mutmut_18, 
        'xǁTaskRepositoryǁget_upcoming__mutmut_19': xǁTaskRepositoryǁget_upcoming__mutmut_19, 
        'xǁTaskRepositoryǁget_upcoming__mutmut_20': xǁTaskRepositoryǁget_upcoming__mutmut_20, 
        'xǁTaskRepositoryǁget_upcoming__mutmut_21': xǁTaskRepositoryǁget_upcoming__mutmut_21, 
        'xǁTaskRepositoryǁget_upcoming__mutmut_22': xǁTaskRepositoryǁget_upcoming__mutmut_22, 
        'xǁTaskRepositoryǁget_upcoming__mutmut_23': xǁTaskRepositoryǁget_upcoming__mutmut_23, 
        'xǁTaskRepositoryǁget_upcoming__mutmut_24': xǁTaskRepositoryǁget_upcoming__mutmut_24
    }
    xǁTaskRepositoryǁget_upcoming__mutmut_orig.__name__ = 'xǁTaskRepositoryǁget_upcoming'

    def update(self, task: Task) -> Task:
        args = [task]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskRepositoryǁupdate__mutmut_orig'), object.__getattribute__(self, 'xǁTaskRepositoryǁupdate__mutmut_mutants'), args, kwargs, self)

    def xǁTaskRepositoryǁupdate__mutmut_orig(self, task: Task) -> Task:
        """Update an existing task."""
        task.updated_at = datetime.now(timezone.utc)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def xǁTaskRepositoryǁupdate__mutmut_1(self, task: Task) -> Task:
        """Update an existing task."""
        task.updated_at = None
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def xǁTaskRepositoryǁupdate__mutmut_2(self, task: Task) -> Task:
        """Update an existing task."""
        task.updated_at = datetime.now(None)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def xǁTaskRepositoryǁupdate__mutmut_3(self, task: Task) -> Task:
        """Update an existing task."""
        task.updated_at = datetime.now(timezone.utc)
        self.session.add(None)
        self.session.commit()
        self.session.refresh(task)
        return task

    def xǁTaskRepositoryǁupdate__mutmut_4(self, task: Task) -> Task:
        """Update an existing task."""
        task.updated_at = datetime.now(timezone.utc)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(None)
        return task
    
    xǁTaskRepositoryǁupdate__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskRepositoryǁupdate__mutmut_1': xǁTaskRepositoryǁupdate__mutmut_1, 
        'xǁTaskRepositoryǁupdate__mutmut_2': xǁTaskRepositoryǁupdate__mutmut_2, 
        'xǁTaskRepositoryǁupdate__mutmut_3': xǁTaskRepositoryǁupdate__mutmut_3, 
        'xǁTaskRepositoryǁupdate__mutmut_4': xǁTaskRepositoryǁupdate__mutmut_4
    }
    xǁTaskRepositoryǁupdate__mutmut_orig.__name__ = 'xǁTaskRepositoryǁupdate'

    def count_total(self) -> int:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskRepositoryǁcount_total__mutmut_orig'), object.__getattribute__(self, 'xǁTaskRepositoryǁcount_total__mutmut_mutants'), args, kwargs, self)

    def xǁTaskRepositoryǁcount_total__mutmut_orig(self) -> int:
        """Return total number of tasks."""
        return self.session.exec(select(func.count(Task.id))).one()

    def xǁTaskRepositoryǁcount_total__mutmut_1(self) -> int:
        """Return total number of tasks."""
        return self.session.exec(None).one()

    def xǁTaskRepositoryǁcount_total__mutmut_2(self) -> int:
        """Return total number of tasks."""
        return self.session.exec(select(None)).one()

    def xǁTaskRepositoryǁcount_total__mutmut_3(self) -> int:
        """Return total number of tasks."""
        return self.session.exec(select(func.count(None))).one()
    
    xǁTaskRepositoryǁcount_total__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskRepositoryǁcount_total__mutmut_1': xǁTaskRepositoryǁcount_total__mutmut_1, 
        'xǁTaskRepositoryǁcount_total__mutmut_2': xǁTaskRepositoryǁcount_total__mutmut_2, 
        'xǁTaskRepositoryǁcount_total__mutmut_3': xǁTaskRepositoryǁcount_total__mutmut_3
    }
    xǁTaskRepositoryǁcount_total__mutmut_orig.__name__ = 'xǁTaskRepositoryǁcount_total'

    def count_by_status(self) -> list[tuple]:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskRepositoryǁcount_by_status__mutmut_orig'), object.__getattribute__(self, 'xǁTaskRepositoryǁcount_by_status__mutmut_mutants'), args, kwargs, self)

    def xǁTaskRepositoryǁcount_by_status__mutmut_orig(self) -> list[tuple]:
        """Return list of (status, count) tuples."""
        return self.session.exec(
            select(Task.status, func.count(Task.id)).group_by(Task.status)
        ).all()

    def xǁTaskRepositoryǁcount_by_status__mutmut_1(self) -> list[tuple]:
        """Return list of (status, count) tuples."""
        return self.session.exec(
            None
        ).all()

    def xǁTaskRepositoryǁcount_by_status__mutmut_2(self) -> list[tuple]:
        """Return list of (status, count) tuples."""
        return self.session.exec(
            select(Task.status, func.count(Task.id)).group_by(None)
        ).all()

    def xǁTaskRepositoryǁcount_by_status__mutmut_3(self) -> list[tuple]:
        """Return list of (status, count) tuples."""
        return self.session.exec(
            select(None, func.count(Task.id)).group_by(Task.status)
        ).all()

    def xǁTaskRepositoryǁcount_by_status__mutmut_4(self) -> list[tuple]:
        """Return list of (status, count) tuples."""
        return self.session.exec(
            select(Task.status, None).group_by(Task.status)
        ).all()

    def xǁTaskRepositoryǁcount_by_status__mutmut_5(self) -> list[tuple]:
        """Return list of (status, count) tuples."""
        return self.session.exec(
            select(func.count(Task.id)).group_by(Task.status)
        ).all()

    def xǁTaskRepositoryǁcount_by_status__mutmut_6(self) -> list[tuple]:
        """Return list of (status, count) tuples."""
        return self.session.exec(
            select(Task.status, ).group_by(Task.status)
        ).all()

    def xǁTaskRepositoryǁcount_by_status__mutmut_7(self) -> list[tuple]:
        """Return list of (status, count) tuples."""
        return self.session.exec(
            select(Task.status, func.count(None)).group_by(Task.status)
        ).all()
    
    xǁTaskRepositoryǁcount_by_status__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskRepositoryǁcount_by_status__mutmut_1': xǁTaskRepositoryǁcount_by_status__mutmut_1, 
        'xǁTaskRepositoryǁcount_by_status__mutmut_2': xǁTaskRepositoryǁcount_by_status__mutmut_2, 
        'xǁTaskRepositoryǁcount_by_status__mutmut_3': xǁTaskRepositoryǁcount_by_status__mutmut_3, 
        'xǁTaskRepositoryǁcount_by_status__mutmut_4': xǁTaskRepositoryǁcount_by_status__mutmut_4, 
        'xǁTaskRepositoryǁcount_by_status__mutmut_5': xǁTaskRepositoryǁcount_by_status__mutmut_5, 
        'xǁTaskRepositoryǁcount_by_status__mutmut_6': xǁTaskRepositoryǁcount_by_status__mutmut_6, 
        'xǁTaskRepositoryǁcount_by_status__mutmut_7': xǁTaskRepositoryǁcount_by_status__mutmut_7
    }
    xǁTaskRepositoryǁcount_by_status__mutmut_orig.__name__ = 'xǁTaskRepositoryǁcount_by_status'

    def count_by_priority(self) -> list[tuple]:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskRepositoryǁcount_by_priority__mutmut_orig'), object.__getattribute__(self, 'xǁTaskRepositoryǁcount_by_priority__mutmut_mutants'), args, kwargs, self)

    def xǁTaskRepositoryǁcount_by_priority__mutmut_orig(self) -> list[tuple]:
        """Return list of (priority, count) tuples."""
        return self.session.exec(
            select(Task.priority, func.count(Task.id)).group_by(Task.priority)
        ).all()

    def xǁTaskRepositoryǁcount_by_priority__mutmut_1(self) -> list[tuple]:
        """Return list of (priority, count) tuples."""
        return self.session.exec(
            None
        ).all()

    def xǁTaskRepositoryǁcount_by_priority__mutmut_2(self) -> list[tuple]:
        """Return list of (priority, count) tuples."""
        return self.session.exec(
            select(Task.priority, func.count(Task.id)).group_by(None)
        ).all()

    def xǁTaskRepositoryǁcount_by_priority__mutmut_3(self) -> list[tuple]:
        """Return list of (priority, count) tuples."""
        return self.session.exec(
            select(None, func.count(Task.id)).group_by(Task.priority)
        ).all()

    def xǁTaskRepositoryǁcount_by_priority__mutmut_4(self) -> list[tuple]:
        """Return list of (priority, count) tuples."""
        return self.session.exec(
            select(Task.priority, None).group_by(Task.priority)
        ).all()

    def xǁTaskRepositoryǁcount_by_priority__mutmut_5(self) -> list[tuple]:
        """Return list of (priority, count) tuples."""
        return self.session.exec(
            select(func.count(Task.id)).group_by(Task.priority)
        ).all()

    def xǁTaskRepositoryǁcount_by_priority__mutmut_6(self) -> list[tuple]:
        """Return list of (priority, count) tuples."""
        return self.session.exec(
            select(Task.priority, ).group_by(Task.priority)
        ).all()

    def xǁTaskRepositoryǁcount_by_priority__mutmut_7(self) -> list[tuple]:
        """Return list of (priority, count) tuples."""
        return self.session.exec(
            select(Task.priority, func.count(None)).group_by(Task.priority)
        ).all()
    
    xǁTaskRepositoryǁcount_by_priority__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskRepositoryǁcount_by_priority__mutmut_1': xǁTaskRepositoryǁcount_by_priority__mutmut_1, 
        'xǁTaskRepositoryǁcount_by_priority__mutmut_2': xǁTaskRepositoryǁcount_by_priority__mutmut_2, 
        'xǁTaskRepositoryǁcount_by_priority__mutmut_3': xǁTaskRepositoryǁcount_by_priority__mutmut_3, 
        'xǁTaskRepositoryǁcount_by_priority__mutmut_4': xǁTaskRepositoryǁcount_by_priority__mutmut_4, 
        'xǁTaskRepositoryǁcount_by_priority__mutmut_5': xǁTaskRepositoryǁcount_by_priority__mutmut_5, 
        'xǁTaskRepositoryǁcount_by_priority__mutmut_6': xǁTaskRepositoryǁcount_by_priority__mutmut_6, 
        'xǁTaskRepositoryǁcount_by_priority__mutmut_7': xǁTaskRepositoryǁcount_by_priority__mutmut_7
    }
    xǁTaskRepositoryǁcount_by_priority__mutmut_orig.__name__ = 'xǁTaskRepositoryǁcount_by_priority'

    def delete(self, task_id: int, owner_id: Optional[int] = None) -> bool:
        args = [task_id, owner_id]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskRepositoryǁdelete__mutmut_orig'), object.__getattribute__(self, 'xǁTaskRepositoryǁdelete__mutmut_mutants'), args, kwargs, self)

    def xǁTaskRepositoryǁdelete__mutmut_orig(self, task_id: int, owner_id: Optional[int] = None) -> bool:
        """Delete a task by ID, optionally scoped to an owner."""
        task = self.get_by_id(task_id, owner_id=owner_id)
        if task:
            self.session.delete(task)
            self.session.commit()
            return True
        return False

    def xǁTaskRepositoryǁdelete__mutmut_1(self, task_id: int, owner_id: Optional[int] = None) -> bool:
        """Delete a task by ID, optionally scoped to an owner."""
        task = None
        if task:
            self.session.delete(task)
            self.session.commit()
            return True
        return False

    def xǁTaskRepositoryǁdelete__mutmut_2(self, task_id: int, owner_id: Optional[int] = None) -> bool:
        """Delete a task by ID, optionally scoped to an owner."""
        task = self.get_by_id(None, owner_id=owner_id)
        if task:
            self.session.delete(task)
            self.session.commit()
            return True
        return False

    def xǁTaskRepositoryǁdelete__mutmut_3(self, task_id: int, owner_id: Optional[int] = None) -> bool:
        """Delete a task by ID, optionally scoped to an owner."""
        task = self.get_by_id(task_id, owner_id=None)
        if task:
            self.session.delete(task)
            self.session.commit()
            return True
        return False

    def xǁTaskRepositoryǁdelete__mutmut_4(self, task_id: int, owner_id: Optional[int] = None) -> bool:
        """Delete a task by ID, optionally scoped to an owner."""
        task = self.get_by_id(owner_id=owner_id)
        if task:
            self.session.delete(task)
            self.session.commit()
            return True
        return False

    def xǁTaskRepositoryǁdelete__mutmut_5(self, task_id: int, owner_id: Optional[int] = None) -> bool:
        """Delete a task by ID, optionally scoped to an owner."""
        task = self.get_by_id(task_id, )
        if task:
            self.session.delete(task)
            self.session.commit()
            return True
        return False

    def xǁTaskRepositoryǁdelete__mutmut_6(self, task_id: int, owner_id: Optional[int] = None) -> bool:
        """Delete a task by ID, optionally scoped to an owner."""
        task = self.get_by_id(task_id, owner_id=owner_id)
        if task:
            self.session.delete(None)
            self.session.commit()
            return True
        return False

    def xǁTaskRepositoryǁdelete__mutmut_7(self, task_id: int, owner_id: Optional[int] = None) -> bool:
        """Delete a task by ID, optionally scoped to an owner."""
        task = self.get_by_id(task_id, owner_id=owner_id)
        if task:
            self.session.delete(task)
            self.session.commit()
            return False
        return False

    def xǁTaskRepositoryǁdelete__mutmut_8(self, task_id: int, owner_id: Optional[int] = None) -> bool:
        """Delete a task by ID, optionally scoped to an owner."""
        task = self.get_by_id(task_id, owner_id=owner_id)
        if task:
            self.session.delete(task)
            self.session.commit()
            return True
        return True
    
    xǁTaskRepositoryǁdelete__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskRepositoryǁdelete__mutmut_1': xǁTaskRepositoryǁdelete__mutmut_1, 
        'xǁTaskRepositoryǁdelete__mutmut_2': xǁTaskRepositoryǁdelete__mutmut_2, 
        'xǁTaskRepositoryǁdelete__mutmut_3': xǁTaskRepositoryǁdelete__mutmut_3, 
        'xǁTaskRepositoryǁdelete__mutmut_4': xǁTaskRepositoryǁdelete__mutmut_4, 
        'xǁTaskRepositoryǁdelete__mutmut_5': xǁTaskRepositoryǁdelete__mutmut_5, 
        'xǁTaskRepositoryǁdelete__mutmut_6': xǁTaskRepositoryǁdelete__mutmut_6, 
        'xǁTaskRepositoryǁdelete__mutmut_7': xǁTaskRepositoryǁdelete__mutmut_7, 
        'xǁTaskRepositoryǁdelete__mutmut_8': xǁTaskRepositoryǁdelete__mutmut_8
    }
    xǁTaskRepositoryǁdelete__mutmut_orig.__name__ = 'xǁTaskRepositoryǁdelete'


class TaskHistoryRepository:
    """Repository for task history tracking."""

    def __init__(self, session: Session) -> None:
        args = [session]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskHistoryRepositoryǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁTaskHistoryRepositoryǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁTaskHistoryRepositoryǁ__init____mutmut_orig(self, session: Session) -> None:
        """Initialize repository with database session."""
        self.session = session

    def xǁTaskHistoryRepositoryǁ__init____mutmut_1(self, session: Session) -> None:
        """Initialize repository with database session."""
        self.session = None
    
    xǁTaskHistoryRepositoryǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskHistoryRepositoryǁ__init____mutmut_1': xǁTaskHistoryRepositoryǁ__init____mutmut_1
    }
    xǁTaskHistoryRepositoryǁ__init____mutmut_orig.__name__ = 'xǁTaskHistoryRepositoryǁ__init__'

    def create(
        self,
        task_id: int,
        user_id: int,
        field_name: str,
        old_value: Optional[str],
        new_value: Optional[str],
    ) -> TaskHistory:
        args = [task_id, user_id, field_name, old_value, new_value]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskHistoryRepositoryǁcreate__mutmut_orig'), object.__getattribute__(self, 'xǁTaskHistoryRepositoryǁcreate__mutmut_mutants'), args, kwargs, self)

    def xǁTaskHistoryRepositoryǁcreate__mutmut_orig(
        self,
        task_id: int,
        user_id: int,
        field_name: str,
        old_value: Optional[str],
        new_value: Optional[str],
    ) -> TaskHistory:
        """Create a new history entry."""
        history = TaskHistory(
            task_id=task_id,
            user_id=user_id,
            field_name=field_name,
            old_value=old_value,
            new_value=new_value,
        )
        self.session.add(history)
        self.session.commit()
        self.session.refresh(history)
        return history

    def xǁTaskHistoryRepositoryǁcreate__mutmut_1(
        self,
        task_id: int,
        user_id: int,
        field_name: str,
        old_value: Optional[str],
        new_value: Optional[str],
    ) -> TaskHistory:
        """Create a new history entry."""
        history = None
        self.session.add(history)
        self.session.commit()
        self.session.refresh(history)
        return history

    def xǁTaskHistoryRepositoryǁcreate__mutmut_2(
        self,
        task_id: int,
        user_id: int,
        field_name: str,
        old_value: Optional[str],
        new_value: Optional[str],
    ) -> TaskHistory:
        """Create a new history entry."""
        history = TaskHistory(
            task_id=None,
            user_id=user_id,
            field_name=field_name,
            old_value=old_value,
            new_value=new_value,
        )
        self.session.add(history)
        self.session.commit()
        self.session.refresh(history)
        return history

    def xǁTaskHistoryRepositoryǁcreate__mutmut_3(
        self,
        task_id: int,
        user_id: int,
        field_name: str,
        old_value: Optional[str],
        new_value: Optional[str],
    ) -> TaskHistory:
        """Create a new history entry."""
        history = TaskHistory(
            task_id=task_id,
            user_id=None,
            field_name=field_name,
            old_value=old_value,
            new_value=new_value,
        )
        self.session.add(history)
        self.session.commit()
        self.session.refresh(history)
        return history

    def xǁTaskHistoryRepositoryǁcreate__mutmut_4(
        self,
        task_id: int,
        user_id: int,
        field_name: str,
        old_value: Optional[str],
        new_value: Optional[str],
    ) -> TaskHistory:
        """Create a new history entry."""
        history = TaskHistory(
            task_id=task_id,
            user_id=user_id,
            field_name=None,
            old_value=old_value,
            new_value=new_value,
        )
        self.session.add(history)
        self.session.commit()
        self.session.refresh(history)
        return history

    def xǁTaskHistoryRepositoryǁcreate__mutmut_5(
        self,
        task_id: int,
        user_id: int,
        field_name: str,
        old_value: Optional[str],
        new_value: Optional[str],
    ) -> TaskHistory:
        """Create a new history entry."""
        history = TaskHistory(
            task_id=task_id,
            user_id=user_id,
            field_name=field_name,
            old_value=None,
            new_value=new_value,
        )
        self.session.add(history)
        self.session.commit()
        self.session.refresh(history)
        return history

    def xǁTaskHistoryRepositoryǁcreate__mutmut_6(
        self,
        task_id: int,
        user_id: int,
        field_name: str,
        old_value: Optional[str],
        new_value: Optional[str],
    ) -> TaskHistory:
        """Create a new history entry."""
        history = TaskHistory(
            task_id=task_id,
            user_id=user_id,
            field_name=field_name,
            old_value=old_value,
            new_value=None,
        )
        self.session.add(history)
        self.session.commit()
        self.session.refresh(history)
        return history

    def xǁTaskHistoryRepositoryǁcreate__mutmut_7(
        self,
        task_id: int,
        user_id: int,
        field_name: str,
        old_value: Optional[str],
        new_value: Optional[str],
    ) -> TaskHistory:
        """Create a new history entry."""
        history = TaskHistory(
            user_id=user_id,
            field_name=field_name,
            old_value=old_value,
            new_value=new_value,
        )
        self.session.add(history)
        self.session.commit()
        self.session.refresh(history)
        return history

    def xǁTaskHistoryRepositoryǁcreate__mutmut_8(
        self,
        task_id: int,
        user_id: int,
        field_name: str,
        old_value: Optional[str],
        new_value: Optional[str],
    ) -> TaskHistory:
        """Create a new history entry."""
        history = TaskHistory(
            task_id=task_id,
            field_name=field_name,
            old_value=old_value,
            new_value=new_value,
        )
        self.session.add(history)
        self.session.commit()
        self.session.refresh(history)
        return history

    def xǁTaskHistoryRepositoryǁcreate__mutmut_9(
        self,
        task_id: int,
        user_id: int,
        field_name: str,
        old_value: Optional[str],
        new_value: Optional[str],
    ) -> TaskHistory:
        """Create a new history entry."""
        history = TaskHistory(
            task_id=task_id,
            user_id=user_id,
            old_value=old_value,
            new_value=new_value,
        )
        self.session.add(history)
        self.session.commit()
        self.session.refresh(history)
        return history

    def xǁTaskHistoryRepositoryǁcreate__mutmut_10(
        self,
        task_id: int,
        user_id: int,
        field_name: str,
        old_value: Optional[str],
        new_value: Optional[str],
    ) -> TaskHistory:
        """Create a new history entry."""
        history = TaskHistory(
            task_id=task_id,
            user_id=user_id,
            field_name=field_name,
            new_value=new_value,
        )
        self.session.add(history)
        self.session.commit()
        self.session.refresh(history)
        return history

    def xǁTaskHistoryRepositoryǁcreate__mutmut_11(
        self,
        task_id: int,
        user_id: int,
        field_name: str,
        old_value: Optional[str],
        new_value: Optional[str],
    ) -> TaskHistory:
        """Create a new history entry."""
        history = TaskHistory(
            task_id=task_id,
            user_id=user_id,
            field_name=field_name,
            old_value=old_value,
            )
        self.session.add(history)
        self.session.commit()
        self.session.refresh(history)
        return history

    def xǁTaskHistoryRepositoryǁcreate__mutmut_12(
        self,
        task_id: int,
        user_id: int,
        field_name: str,
        old_value: Optional[str],
        new_value: Optional[str],
    ) -> TaskHistory:
        """Create a new history entry."""
        history = TaskHistory(
            task_id=task_id,
            user_id=user_id,
            field_name=field_name,
            old_value=old_value,
            new_value=new_value,
        )
        self.session.add(None)
        self.session.commit()
        self.session.refresh(history)
        return history

    def xǁTaskHistoryRepositoryǁcreate__mutmut_13(
        self,
        task_id: int,
        user_id: int,
        field_name: str,
        old_value: Optional[str],
        new_value: Optional[str],
    ) -> TaskHistory:
        """Create a new history entry."""
        history = TaskHistory(
            task_id=task_id,
            user_id=user_id,
            field_name=field_name,
            old_value=old_value,
            new_value=new_value,
        )
        self.session.add(history)
        self.session.commit()
        self.session.refresh(None)
        return history
    
    xǁTaskHistoryRepositoryǁcreate__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskHistoryRepositoryǁcreate__mutmut_1': xǁTaskHistoryRepositoryǁcreate__mutmut_1, 
        'xǁTaskHistoryRepositoryǁcreate__mutmut_2': xǁTaskHistoryRepositoryǁcreate__mutmut_2, 
        'xǁTaskHistoryRepositoryǁcreate__mutmut_3': xǁTaskHistoryRepositoryǁcreate__mutmut_3, 
        'xǁTaskHistoryRepositoryǁcreate__mutmut_4': xǁTaskHistoryRepositoryǁcreate__mutmut_4, 
        'xǁTaskHistoryRepositoryǁcreate__mutmut_5': xǁTaskHistoryRepositoryǁcreate__mutmut_5, 
        'xǁTaskHistoryRepositoryǁcreate__mutmut_6': xǁTaskHistoryRepositoryǁcreate__mutmut_6, 
        'xǁTaskHistoryRepositoryǁcreate__mutmut_7': xǁTaskHistoryRepositoryǁcreate__mutmut_7, 
        'xǁTaskHistoryRepositoryǁcreate__mutmut_8': xǁTaskHistoryRepositoryǁcreate__mutmut_8, 
        'xǁTaskHistoryRepositoryǁcreate__mutmut_9': xǁTaskHistoryRepositoryǁcreate__mutmut_9, 
        'xǁTaskHistoryRepositoryǁcreate__mutmut_10': xǁTaskHistoryRepositoryǁcreate__mutmut_10, 
        'xǁTaskHistoryRepositoryǁcreate__mutmut_11': xǁTaskHistoryRepositoryǁcreate__mutmut_11, 
        'xǁTaskHistoryRepositoryǁcreate__mutmut_12': xǁTaskHistoryRepositoryǁcreate__mutmut_12, 
        'xǁTaskHistoryRepositoryǁcreate__mutmut_13': xǁTaskHistoryRepositoryǁcreate__mutmut_13
    }
    xǁTaskHistoryRepositoryǁcreate__mutmut_orig.__name__ = 'xǁTaskHistoryRepositoryǁcreate'

    def get_by_task(self, task_id: int) -> list[TaskHistory]:
        args = [task_id]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskHistoryRepositoryǁget_by_task__mutmut_orig'), object.__getattribute__(self, 'xǁTaskHistoryRepositoryǁget_by_task__mutmut_mutants'), args, kwargs, self)

    def xǁTaskHistoryRepositoryǁget_by_task__mutmut_orig(self, task_id: int) -> list[TaskHistory]:
        """Get all history entries for a task, ordered by date."""
        statement = (
            select(TaskHistory)
            .where(TaskHistory.task_id == task_id)
            .order_by(TaskHistory.changed_at)
        )
        return list(self.session.exec(statement).all())

    def xǁTaskHistoryRepositoryǁget_by_task__mutmut_1(self, task_id: int) -> list[TaskHistory]:
        """Get all history entries for a task, ordered by date."""
        statement = None
        return list(self.session.exec(statement).all())

    def xǁTaskHistoryRepositoryǁget_by_task__mutmut_2(self, task_id: int) -> list[TaskHistory]:
        """Get all history entries for a task, ordered by date."""
        statement = (
            select(TaskHistory)
            .where(TaskHistory.task_id == task_id)
            .order_by(None)
        )
        return list(self.session.exec(statement).all())

    def xǁTaskHistoryRepositoryǁget_by_task__mutmut_3(self, task_id: int) -> list[TaskHistory]:
        """Get all history entries for a task, ordered by date."""
        statement = (
            select(TaskHistory)
            .where(None)
            .order_by(TaskHistory.changed_at)
        )
        return list(self.session.exec(statement).all())

    def xǁTaskHistoryRepositoryǁget_by_task__mutmut_4(self, task_id: int) -> list[TaskHistory]:
        """Get all history entries for a task, ordered by date."""
        statement = (
            select(None)
            .where(TaskHistory.task_id == task_id)
            .order_by(TaskHistory.changed_at)
        )
        return list(self.session.exec(statement).all())

    def xǁTaskHistoryRepositoryǁget_by_task__mutmut_5(self, task_id: int) -> list[TaskHistory]:
        """Get all history entries for a task, ordered by date."""
        statement = (
            select(TaskHistory)
            .where(TaskHistory.task_id != task_id)
            .order_by(TaskHistory.changed_at)
        )
        return list(self.session.exec(statement).all())

    def xǁTaskHistoryRepositoryǁget_by_task__mutmut_6(self, task_id: int) -> list[TaskHistory]:
        """Get all history entries for a task, ordered by date."""
        statement = (
            select(TaskHistory)
            .where(TaskHistory.task_id == task_id)
            .order_by(TaskHistory.changed_at)
        )
        return list(None)

    def xǁTaskHistoryRepositoryǁget_by_task__mutmut_7(self, task_id: int) -> list[TaskHistory]:
        """Get all history entries for a task, ordered by date."""
        statement = (
            select(TaskHistory)
            .where(TaskHistory.task_id == task_id)
            .order_by(TaskHistory.changed_at)
        )
        return list(self.session.exec(None).all())
    
    xǁTaskHistoryRepositoryǁget_by_task__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskHistoryRepositoryǁget_by_task__mutmut_1': xǁTaskHistoryRepositoryǁget_by_task__mutmut_1, 
        'xǁTaskHistoryRepositoryǁget_by_task__mutmut_2': xǁTaskHistoryRepositoryǁget_by_task__mutmut_2, 
        'xǁTaskHistoryRepositoryǁget_by_task__mutmut_3': xǁTaskHistoryRepositoryǁget_by_task__mutmut_3, 
        'xǁTaskHistoryRepositoryǁget_by_task__mutmut_4': xǁTaskHistoryRepositoryǁget_by_task__mutmut_4, 
        'xǁTaskHistoryRepositoryǁget_by_task__mutmut_5': xǁTaskHistoryRepositoryǁget_by_task__mutmut_5, 
        'xǁTaskHistoryRepositoryǁget_by_task__mutmut_6': xǁTaskHistoryRepositoryǁget_by_task__mutmut_6, 
        'xǁTaskHistoryRepositoryǁget_by_task__mutmut_7': xǁTaskHistoryRepositoryǁget_by_task__mutmut_7
    }
    xǁTaskHistoryRepositoryǁget_by_task__mutmut_orig.__name__ = 'xǁTaskHistoryRepositoryǁget_by_task'


class TaskCommentRepository:
    """Repository for task comments."""

    def __init__(self, session: Session) -> None:
        args = [session]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskCommentRepositoryǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁTaskCommentRepositoryǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁTaskCommentRepositoryǁ__init____mutmut_orig(self, session: Session) -> None:
        """Initialize repository with database session."""
        self.session = session

    def xǁTaskCommentRepositoryǁ__init____mutmut_1(self, session: Session) -> None:
        """Initialize repository with database session."""
        self.session = None
    
    xǁTaskCommentRepositoryǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskCommentRepositoryǁ__init____mutmut_1': xǁTaskCommentRepositoryǁ__init____mutmut_1
    }
    xǁTaskCommentRepositoryǁ__init____mutmut_orig.__name__ = 'xǁTaskCommentRepositoryǁ__init__'

    def create(self, task_id: int, user_id: int, content: str) -> TaskComment:
        args = [task_id, user_id, content]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskCommentRepositoryǁcreate__mutmut_orig'), object.__getattribute__(self, 'xǁTaskCommentRepositoryǁcreate__mutmut_mutants'), args, kwargs, self)

    def xǁTaskCommentRepositoryǁcreate__mutmut_orig(self, task_id: int, user_id: int, content: str) -> TaskComment:
        """Create a new comment."""
        comment = TaskComment(task_id=task_id, user_id=user_id, content=content)
        self.session.add(comment)
        self.session.commit()
        self.session.refresh(comment)
        return comment

    def xǁTaskCommentRepositoryǁcreate__mutmut_1(self, task_id: int, user_id: int, content: str) -> TaskComment:
        """Create a new comment."""
        comment = None
        self.session.add(comment)
        self.session.commit()
        self.session.refresh(comment)
        return comment

    def xǁTaskCommentRepositoryǁcreate__mutmut_2(self, task_id: int, user_id: int, content: str) -> TaskComment:
        """Create a new comment."""
        comment = TaskComment(task_id=None, user_id=user_id, content=content)
        self.session.add(comment)
        self.session.commit()
        self.session.refresh(comment)
        return comment

    def xǁTaskCommentRepositoryǁcreate__mutmut_3(self, task_id: int, user_id: int, content: str) -> TaskComment:
        """Create a new comment."""
        comment = TaskComment(task_id=task_id, user_id=None, content=content)
        self.session.add(comment)
        self.session.commit()
        self.session.refresh(comment)
        return comment

    def xǁTaskCommentRepositoryǁcreate__mutmut_4(self, task_id: int, user_id: int, content: str) -> TaskComment:
        """Create a new comment."""
        comment = TaskComment(task_id=task_id, user_id=user_id, content=None)
        self.session.add(comment)
        self.session.commit()
        self.session.refresh(comment)
        return comment

    def xǁTaskCommentRepositoryǁcreate__mutmut_5(self, task_id: int, user_id: int, content: str) -> TaskComment:
        """Create a new comment."""
        comment = TaskComment(user_id=user_id, content=content)
        self.session.add(comment)
        self.session.commit()
        self.session.refresh(comment)
        return comment

    def xǁTaskCommentRepositoryǁcreate__mutmut_6(self, task_id: int, user_id: int, content: str) -> TaskComment:
        """Create a new comment."""
        comment = TaskComment(task_id=task_id, content=content)
        self.session.add(comment)
        self.session.commit()
        self.session.refresh(comment)
        return comment

    def xǁTaskCommentRepositoryǁcreate__mutmut_7(self, task_id: int, user_id: int, content: str) -> TaskComment:
        """Create a new comment."""
        comment = TaskComment(task_id=task_id, user_id=user_id, )
        self.session.add(comment)
        self.session.commit()
        self.session.refresh(comment)
        return comment

    def xǁTaskCommentRepositoryǁcreate__mutmut_8(self, task_id: int, user_id: int, content: str) -> TaskComment:
        """Create a new comment."""
        comment = TaskComment(task_id=task_id, user_id=user_id, content=content)
        self.session.add(None)
        self.session.commit()
        self.session.refresh(comment)
        return comment

    def xǁTaskCommentRepositoryǁcreate__mutmut_9(self, task_id: int, user_id: int, content: str) -> TaskComment:
        """Create a new comment."""
        comment = TaskComment(task_id=task_id, user_id=user_id, content=content)
        self.session.add(comment)
        self.session.commit()
        self.session.refresh(None)
        return comment
    
    xǁTaskCommentRepositoryǁcreate__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskCommentRepositoryǁcreate__mutmut_1': xǁTaskCommentRepositoryǁcreate__mutmut_1, 
        'xǁTaskCommentRepositoryǁcreate__mutmut_2': xǁTaskCommentRepositoryǁcreate__mutmut_2, 
        'xǁTaskCommentRepositoryǁcreate__mutmut_3': xǁTaskCommentRepositoryǁcreate__mutmut_3, 
        'xǁTaskCommentRepositoryǁcreate__mutmut_4': xǁTaskCommentRepositoryǁcreate__mutmut_4, 
        'xǁTaskCommentRepositoryǁcreate__mutmut_5': xǁTaskCommentRepositoryǁcreate__mutmut_5, 
        'xǁTaskCommentRepositoryǁcreate__mutmut_6': xǁTaskCommentRepositoryǁcreate__mutmut_6, 
        'xǁTaskCommentRepositoryǁcreate__mutmut_7': xǁTaskCommentRepositoryǁcreate__mutmut_7, 
        'xǁTaskCommentRepositoryǁcreate__mutmut_8': xǁTaskCommentRepositoryǁcreate__mutmut_8, 
        'xǁTaskCommentRepositoryǁcreate__mutmut_9': xǁTaskCommentRepositoryǁcreate__mutmut_9
    }
    xǁTaskCommentRepositoryǁcreate__mutmut_orig.__name__ = 'xǁTaskCommentRepositoryǁcreate'

    def get_by_task(self, task_id: int) -> list[TaskComment]:
        args = [task_id]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskCommentRepositoryǁget_by_task__mutmut_orig'), object.__getattribute__(self, 'xǁTaskCommentRepositoryǁget_by_task__mutmut_mutants'), args, kwargs, self)

    def xǁTaskCommentRepositoryǁget_by_task__mutmut_orig(self, task_id: int) -> list[TaskComment]:
        """Get all comments for a task, ordered by date."""
        statement = (
            select(TaskComment)
            .where(TaskComment.task_id == task_id)
            .order_by(TaskComment.created_at)
        )
        return list(self.session.exec(statement).all())

    def xǁTaskCommentRepositoryǁget_by_task__mutmut_1(self, task_id: int) -> list[TaskComment]:
        """Get all comments for a task, ordered by date."""
        statement = None
        return list(self.session.exec(statement).all())

    def xǁTaskCommentRepositoryǁget_by_task__mutmut_2(self, task_id: int) -> list[TaskComment]:
        """Get all comments for a task, ordered by date."""
        statement = (
            select(TaskComment)
            .where(TaskComment.task_id == task_id)
            .order_by(None)
        )
        return list(self.session.exec(statement).all())

    def xǁTaskCommentRepositoryǁget_by_task__mutmut_3(self, task_id: int) -> list[TaskComment]:
        """Get all comments for a task, ordered by date."""
        statement = (
            select(TaskComment)
            .where(None)
            .order_by(TaskComment.created_at)
        )
        return list(self.session.exec(statement).all())

    def xǁTaskCommentRepositoryǁget_by_task__mutmut_4(self, task_id: int) -> list[TaskComment]:
        """Get all comments for a task, ordered by date."""
        statement = (
            select(None)
            .where(TaskComment.task_id == task_id)
            .order_by(TaskComment.created_at)
        )
        return list(self.session.exec(statement).all())

    def xǁTaskCommentRepositoryǁget_by_task__mutmut_5(self, task_id: int) -> list[TaskComment]:
        """Get all comments for a task, ordered by date."""
        statement = (
            select(TaskComment)
            .where(TaskComment.task_id != task_id)
            .order_by(TaskComment.created_at)
        )
        return list(self.session.exec(statement).all())

    def xǁTaskCommentRepositoryǁget_by_task__mutmut_6(self, task_id: int) -> list[TaskComment]:
        """Get all comments for a task, ordered by date."""
        statement = (
            select(TaskComment)
            .where(TaskComment.task_id == task_id)
            .order_by(TaskComment.created_at)
        )
        return list(None)

    def xǁTaskCommentRepositoryǁget_by_task__mutmut_7(self, task_id: int) -> list[TaskComment]:
        """Get all comments for a task, ordered by date."""
        statement = (
            select(TaskComment)
            .where(TaskComment.task_id == task_id)
            .order_by(TaskComment.created_at)
        )
        return list(self.session.exec(None).all())
    
    xǁTaskCommentRepositoryǁget_by_task__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskCommentRepositoryǁget_by_task__mutmut_1': xǁTaskCommentRepositoryǁget_by_task__mutmut_1, 
        'xǁTaskCommentRepositoryǁget_by_task__mutmut_2': xǁTaskCommentRepositoryǁget_by_task__mutmut_2, 
        'xǁTaskCommentRepositoryǁget_by_task__mutmut_3': xǁTaskCommentRepositoryǁget_by_task__mutmut_3, 
        'xǁTaskCommentRepositoryǁget_by_task__mutmut_4': xǁTaskCommentRepositoryǁget_by_task__mutmut_4, 
        'xǁTaskCommentRepositoryǁget_by_task__mutmut_5': xǁTaskCommentRepositoryǁget_by_task__mutmut_5, 
        'xǁTaskCommentRepositoryǁget_by_task__mutmut_6': xǁTaskCommentRepositoryǁget_by_task__mutmut_6, 
        'xǁTaskCommentRepositoryǁget_by_task__mutmut_7': xǁTaskCommentRepositoryǁget_by_task__mutmut_7
    }
    xǁTaskCommentRepositoryǁget_by_task__mutmut_orig.__name__ = 'xǁTaskCommentRepositoryǁget_by_task'
