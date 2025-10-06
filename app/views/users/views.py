from pydantic import ValidationError

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi_users.exceptions import UserAlreadyExists

from api.api_v1.fastapi_users import current_active_user_cookie
from api.dependencies.authentication.user_manager import get_user_manager
from api.dependencies.authentication import authentication_backend_cookie
from api.dependencies.authentication.access_tokens import get_access_tokens_db
from core.models.user import User
from crud.users import authenticate_user
from core.authentication.user_manager import UserManager
from core.schemas.user import UserCreate
from utils.templates import templates


from starlette.status import HTTP_302_FOUND
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix="/user",
    tags=["Users"],
)


@router.get("/register", name="register")
async def register_page(
    request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "title": "Регистрация",
        },
    )


@router.post("/register")
async def register_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    user_manager: UserManager = Depends(get_user_manager),
):
    user_create = UserCreate(
        username=username,
        email=email,
        password=password,
    )

    try:
        await user_manager.create(user_create)
        return RedirectResponse(
            url="/user/login?success=1",
            status_code=HTTP_302_FOUND,
        )
    except UserAlreadyExists:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "title": "Регистрация",
                "error": "Пользователь с таким именем уже существует.",
            },
        )
    except IntegrityError:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "title": "Регистрация",
                "error": "Ошибка регистрации",
            },
        )
    except ValidationError:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": "Ошибка валидации",
            },
        )


@router.get("/login", name="login")
async def login_get(request: Request, success: str = None):

    message = None
    if success == "1":
        message = "Регистрация прошла успешно. Войдите в аккаунт."

    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "success": message,
            "title": "Войти",
        },
    )


@router.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    user_manager: UserManager = Depends(get_user_manager),
    access_tokens_db=Depends(get_access_tokens_db),
):
    user = await authenticate_user(
        email,
        password,
        user_manager,
    )

    if not user:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Неверный логин или пароль",
            },
        )

    strategy = authentication_backend_cookie.get_strategy(
        access_tokens_db=access_tokens_db
    )
    token = await strategy.write_token(user)

    response = RedirectResponse(
        url="/user/profile",
        status_code=HTTP_302_FOUND,
    )
    response.set_cookie(
        "access_token",
        value=token,
        httponly=True,
        max_age=3600,
    )
    return response


@router.get("/profile", name="profile")
async def profile_page(
    request: Request,
    user=Depends(current_active_user_cookie),
):
    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "user": user,
            "title": "Профиль",
        },
    )


@router.get("/logout", name="logout")
async def logout(
    request: Request,
    user: User = Depends(current_active_user_cookie),
    access_tokens_db=Depends(get_access_tokens_db),
):
    strategy = authentication_backend_cookie.get_strategy(
        access_tokens_db=access_tokens_db
    )
    token = request.cookies.get("access_token")

    response = await authentication_backend_cookie.logout(
        strategy,
        user,
        token,
    )
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("access_token")

    return response


# @router.post("/recipes/", response_model=RecipeResponse)
# async def create_recipe(
#     recipe_data: RecipeCreateRequest,
#     session: AsyncSession = Depends(db_helper.session_getter),
#     current_user: User = Depends(current_active_user_bearer),
# ):
#     print("Incoming recipe_data:", recipe_data)

#     associations = []
#     for pi in recipe_data.products_info:
#         if pi.calories_per_unit is None:
#             product = await session.get(Product, pi.product_id)
#             if not product:
#                 raise HTTPException(404, "Продукт не найден")
#             cal = product.calories_per_unit
#         else:
#             cal = pi.calories_per_unit

#         assoc = RecipeProductAssociation(
#             product_id=pi.product_id,
#             quantity=pi.quantity,
#             calories_per_unit=cal,
#         )
#         associations.append(assoc)

#     recipe = Recipe(
#         title=recipe_data.title,
#         body=recipe_data.body,
#         user_id=current_user.id,
#     )
#     session.add(recipe)
#     await session.flush()

#     for assoc in associations:
#         assoc.recipe_id = recipe.id
#         session.add(assoc)

#     await session.commit()

#     result = await session.execute(
#         select(Recipe)
#         .options(selectinload(Recipe.product_associations))
#         .where(Recipe.id == recipe.id)
#     )
#     created = result.scalar_one()
#     return created
