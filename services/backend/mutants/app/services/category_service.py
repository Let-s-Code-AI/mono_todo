"""Business logic layer for category operations."""

from typing import Optional

from app.db.models import Category
from app.db.repository import CategoryRepository
from app.schemas.task import CategoryCreate
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


class CategoryService:
    """Service layer for category business logic."""

    def __init__(self, repository: CategoryRepository) -> None:
        args = [repository]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCategoryServiceǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁCategoryServiceǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁCategoryServiceǁ__init____mutmut_orig(self, repository: CategoryRepository) -> None:
        self.repository = repository

    def xǁCategoryServiceǁ__init____mutmut_1(self, repository: CategoryRepository) -> None:
        self.repository = None
    
    xǁCategoryServiceǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCategoryServiceǁ__init____mutmut_1': xǁCategoryServiceǁ__init____mutmut_1
    }
    xǁCategoryServiceǁ__init____mutmut_orig.__name__ = 'xǁCategoryServiceǁ__init__'

    def create_category(self, data: CategoryCreate) -> tuple[Category, bool]:
        args = [data]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCategoryServiceǁcreate_category__mutmut_orig'), object.__getattribute__(self, 'xǁCategoryServiceǁcreate_category__mutmut_mutants'), args, kwargs, self)

    def xǁCategoryServiceǁcreate_category__mutmut_orig(self, data: CategoryCreate) -> tuple[Category, bool]:
        """
        Create a new category.

        Returns:
            Tuple of (category, created) where created=False means name already exists.
        """
        existing = self.repository.get_by_name(data.name)
        if existing:
            return existing, False
        category = Category(name=data.name, color=data.color)
        return self.repository.create(category), True

    def xǁCategoryServiceǁcreate_category__mutmut_1(self, data: CategoryCreate) -> tuple[Category, bool]:
        """
        Create a new category.

        Returns:
            Tuple of (category, created) where created=False means name already exists.
        """
        existing = None
        if existing:
            return existing, False
        category = Category(name=data.name, color=data.color)
        return self.repository.create(category), True

    def xǁCategoryServiceǁcreate_category__mutmut_2(self, data: CategoryCreate) -> tuple[Category, bool]:
        """
        Create a new category.

        Returns:
            Tuple of (category, created) where created=False means name already exists.
        """
        existing = self.repository.get_by_name(None)
        if existing:
            return existing, False
        category = Category(name=data.name, color=data.color)
        return self.repository.create(category), True

    def xǁCategoryServiceǁcreate_category__mutmut_3(self, data: CategoryCreate) -> tuple[Category, bool]:
        """
        Create a new category.

        Returns:
            Tuple of (category, created) where created=False means name already exists.
        """
        existing = self.repository.get_by_name(data.name)
        if existing:
            return existing, True
        category = Category(name=data.name, color=data.color)
        return self.repository.create(category), True

    def xǁCategoryServiceǁcreate_category__mutmut_4(self, data: CategoryCreate) -> tuple[Category, bool]:
        """
        Create a new category.

        Returns:
            Tuple of (category, created) where created=False means name already exists.
        """
        existing = self.repository.get_by_name(data.name)
        if existing:
            return existing, False
        category = None
        return self.repository.create(category), True

    def xǁCategoryServiceǁcreate_category__mutmut_5(self, data: CategoryCreate) -> tuple[Category, bool]:
        """
        Create a new category.

        Returns:
            Tuple of (category, created) where created=False means name already exists.
        """
        existing = self.repository.get_by_name(data.name)
        if existing:
            return existing, False
        category = Category(name=None, color=data.color)
        return self.repository.create(category), True

    def xǁCategoryServiceǁcreate_category__mutmut_6(self, data: CategoryCreate) -> tuple[Category, bool]:
        """
        Create a new category.

        Returns:
            Tuple of (category, created) where created=False means name already exists.
        """
        existing = self.repository.get_by_name(data.name)
        if existing:
            return existing, False
        category = Category(name=data.name, color=None)
        return self.repository.create(category), True

    def xǁCategoryServiceǁcreate_category__mutmut_7(self, data: CategoryCreate) -> tuple[Category, bool]:
        """
        Create a new category.

        Returns:
            Tuple of (category, created) where created=False means name already exists.
        """
        existing = self.repository.get_by_name(data.name)
        if existing:
            return existing, False
        category = Category(color=data.color)
        return self.repository.create(category), True

    def xǁCategoryServiceǁcreate_category__mutmut_8(self, data: CategoryCreate) -> tuple[Category, bool]:
        """
        Create a new category.

        Returns:
            Tuple of (category, created) where created=False means name already exists.
        """
        existing = self.repository.get_by_name(data.name)
        if existing:
            return existing, False
        category = Category(name=data.name, )
        return self.repository.create(category), True

    def xǁCategoryServiceǁcreate_category__mutmut_9(self, data: CategoryCreate) -> tuple[Category, bool]:
        """
        Create a new category.

        Returns:
            Tuple of (category, created) where created=False means name already exists.
        """
        existing = self.repository.get_by_name(data.name)
        if existing:
            return existing, False
        category = Category(name=data.name, color=data.color)
        return self.repository.create(None), True

    def xǁCategoryServiceǁcreate_category__mutmut_10(self, data: CategoryCreate) -> tuple[Category, bool]:
        """
        Create a new category.

        Returns:
            Tuple of (category, created) where created=False means name already exists.
        """
        existing = self.repository.get_by_name(data.name)
        if existing:
            return existing, False
        category = Category(name=data.name, color=data.color)
        return self.repository.create(category), False
    
    xǁCategoryServiceǁcreate_category__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCategoryServiceǁcreate_category__mutmut_1': xǁCategoryServiceǁcreate_category__mutmut_1, 
        'xǁCategoryServiceǁcreate_category__mutmut_2': xǁCategoryServiceǁcreate_category__mutmut_2, 
        'xǁCategoryServiceǁcreate_category__mutmut_3': xǁCategoryServiceǁcreate_category__mutmut_3, 
        'xǁCategoryServiceǁcreate_category__mutmut_4': xǁCategoryServiceǁcreate_category__mutmut_4, 
        'xǁCategoryServiceǁcreate_category__mutmut_5': xǁCategoryServiceǁcreate_category__mutmut_5, 
        'xǁCategoryServiceǁcreate_category__mutmut_6': xǁCategoryServiceǁcreate_category__mutmut_6, 
        'xǁCategoryServiceǁcreate_category__mutmut_7': xǁCategoryServiceǁcreate_category__mutmut_7, 
        'xǁCategoryServiceǁcreate_category__mutmut_8': xǁCategoryServiceǁcreate_category__mutmut_8, 
        'xǁCategoryServiceǁcreate_category__mutmut_9': xǁCategoryServiceǁcreate_category__mutmut_9, 
        'xǁCategoryServiceǁcreate_category__mutmut_10': xǁCategoryServiceǁcreate_category__mutmut_10
    }
    xǁCategoryServiceǁcreate_category__mutmut_orig.__name__ = 'xǁCategoryServiceǁcreate_category'

    def delete_category(self, category_id: int) -> Optional[Category]:
        args = [category_id]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCategoryServiceǁdelete_category__mutmut_orig'), object.__getattribute__(self, 'xǁCategoryServiceǁdelete_category__mutmut_mutants'), args, kwargs, self)

    def xǁCategoryServiceǁdelete_category__mutmut_orig(self, category_id: int) -> Optional[Category]:
        """
        Delete a category and nullify all tasks assigned to it.

        Returns:
            The deleted Category if found, None otherwise.
        """
        category = self.repository.get_by_id(category_id)
        if not category:
            return None
        self.repository.delete_and_nullify_tasks(category_id)
        return category

    def xǁCategoryServiceǁdelete_category__mutmut_1(self, category_id: int) -> Optional[Category]:
        """
        Delete a category and nullify all tasks assigned to it.

        Returns:
            The deleted Category if found, None otherwise.
        """
        category = None
        if not category:
            return None
        self.repository.delete_and_nullify_tasks(category_id)
        return category

    def xǁCategoryServiceǁdelete_category__mutmut_2(self, category_id: int) -> Optional[Category]:
        """
        Delete a category and nullify all tasks assigned to it.

        Returns:
            The deleted Category if found, None otherwise.
        """
        category = self.repository.get_by_id(None)
        if not category:
            return None
        self.repository.delete_and_nullify_tasks(category_id)
        return category

    def xǁCategoryServiceǁdelete_category__mutmut_3(self, category_id: int) -> Optional[Category]:
        """
        Delete a category and nullify all tasks assigned to it.

        Returns:
            The deleted Category if found, None otherwise.
        """
        category = self.repository.get_by_id(category_id)
        if category:
            return None
        self.repository.delete_and_nullify_tasks(category_id)
        return category

    def xǁCategoryServiceǁdelete_category__mutmut_4(self, category_id: int) -> Optional[Category]:
        """
        Delete a category and nullify all tasks assigned to it.

        Returns:
            The deleted Category if found, None otherwise.
        """
        category = self.repository.get_by_id(category_id)
        if not category:
            return None
        self.repository.delete_and_nullify_tasks(None)
        return category
    
    xǁCategoryServiceǁdelete_category__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCategoryServiceǁdelete_category__mutmut_1': xǁCategoryServiceǁdelete_category__mutmut_1, 
        'xǁCategoryServiceǁdelete_category__mutmut_2': xǁCategoryServiceǁdelete_category__mutmut_2, 
        'xǁCategoryServiceǁdelete_category__mutmut_3': xǁCategoryServiceǁdelete_category__mutmut_3, 
        'xǁCategoryServiceǁdelete_category__mutmut_4': xǁCategoryServiceǁdelete_category__mutmut_4
    }
    xǁCategoryServiceǁdelete_category__mutmut_orig.__name__ = 'xǁCategoryServiceǁdelete_category'
