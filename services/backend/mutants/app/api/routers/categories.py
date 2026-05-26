"""API routes for category operations."""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.api.deps import get_current_user
from app.db.models import User
from app.db.repository import CategoryRepository
from app.db.session import get_session
from app.schemas.task import CategoryCreate, CategoryResponse
from app.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])
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


def get_category_repository(session: Session = Depends(get_session)) -> CategoryRepository:
    args = [session]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_category_repository__mutmut_orig, x_get_category_repository__mutmut_mutants, args, kwargs, None)


def x_get_category_repository__mutmut_orig(session: Session = Depends(get_session)) -> CategoryRepository:
    return CategoryRepository(session)


def x_get_category_repository__mutmut_1(session: Session = Depends(get_session)) -> CategoryRepository:
    return CategoryRepository(None)

x_get_category_repository__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_category_repository__mutmut_1': x_get_category_repository__mutmut_1
}
x_get_category_repository__mutmut_orig.__name__ = 'x_get_category_repository'


def get_category_service(
    repository: CategoryRepository = Depends(get_category_repository),
) -> CategoryService:
    args = [repository]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_category_service__mutmut_orig, x_get_category_service__mutmut_mutants, args, kwargs, None)


def x_get_category_service__mutmut_orig(
    repository: CategoryRepository = Depends(get_category_repository),
) -> CategoryService:
    return CategoryService(repository)


def x_get_category_service__mutmut_1(
    repository: CategoryRepository = Depends(get_category_repository),
) -> CategoryService:
    return CategoryService(None)

x_get_category_service__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_category_service__mutmut_1': x_get_category_service__mutmut_1
}
x_get_category_service__mutmut_orig.__name__ = 'x_get_category_service'


@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(
    data: CategoryCreate,
    service: CategoryService = Depends(get_category_service),
    _: User = Depends(get_current_user),
) -> CategoryResponse:
    """Create a new category.

    Args:
        data: Category creation data
        service: Category service dependency

    Returns:
        Created category

    Raises:
        HTTPException: 409 if a category with that name already exists
    """
    category, created = service.create_category(data)
    if not created:
        raise HTTPException(status_code=409, detail="Category with this name already exists")
    return CategoryResponse.model_validate(category)


@router.delete("/{category_id}", status_code=200)
def delete_category(
    category_id: int,
    service: CategoryService = Depends(get_category_service),
    _: User = Depends(get_current_user),
) -> dict:
    """Delete a category and nullify category_id on all assigned tasks.

    Args:
        category_id: Category identifier
        service: Category service dependency

    Returns:
        Confirmation message

    Raises:
        HTTPException: 404 if category not found
    """
    category = service.delete_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"detail": "Category deleted"}
