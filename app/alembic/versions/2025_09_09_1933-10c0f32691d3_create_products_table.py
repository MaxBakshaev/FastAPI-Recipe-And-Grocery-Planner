"""create products table, added products list

Revision ID: 10c0f32691d3
Revises: d9feec052f1e
Create Date: 2025-09-09 19:33:09.069181

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "10c0f32691d3"
down_revision: Union[str, Sequence[str], None] = "d9feec052f1e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "products",
        sa.Column("name", sa.String(length=32), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_products")),
    )
    op.create_index(op.f("ix_products_name"), "products", ["name"], unique=True)
    op.create_table(
        "profiles",
        sa.Column("first_name", sa.String(length=40), nullable=True),
        sa.Column("last_name", sa.String(length=40), nullable=True),
        sa.Column("bio", sa.String(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_profiles_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_profiles")),
        sa.UniqueConstraint("user_id", name=op.f("uq_profiles_user_id")),
    )
    op.add_column("users", sa.Column("username", sa.String(length=32), nullable=False))
    op.create_unique_constraint(op.f("uq_users_username"), "users", ["username"])
    op.execute(
        """
        INSERT INTO products (name) VALUES
        ('Яблоко'),
        ('Банан'),
        ('Апельсин'),
        ('Груша'),
        ('Киви'),
        ('Ананас'),
        ('Арбуз'),
        ('Дыня'),
        ('Виноград'),
        ('Клубника'),
        ('Малина'),
        ('Черника'),
        ('Смородина'),
        ('Персик'),
        ('Нектарин'),
        ('Манго'),
        ('Папайя'),
        ('Лимон'),
        ('Лайм'),
        ('Авокадо'),
        ('Картофель'),
        ('Морковь'),
        ('Свёкла'),
        ('Томат'),
        ('Огурец'),
        ('Капуста'),
        ('Брокколи'),
        ('Цветная капуста'),
        ('Лук'),
        ('Чеснок'),
        ('Шпинат'),
        ('Петрушка'),
        ('Укроп'),
        ('Сельдерей'),
        ('Фасоль'),
        ('Горох'),
        ('Чечевица'),
        ('Рис'),
        ('Гречка'),
        ('Овсянка'),
        ('Пшено'),
        ('Макароны'),
        ('Хлеб'),
        ('Булка'),
        ('Мука'),
        ('Сахар'),
        ('Соль'),
        ('Перец чёрный'),
        ('Молоко'),
        ('Сыр'),
        ('Творог'),
        ('Сметана'),
        ('Йогурт'),
        ('Масло сливочное'),
        ('Масло растительное'),
        ('Курица'),
        ('Говядина'),
        ('Свинина'),
        ('Рыба'),
        ('Яйцо'),
        ('Колбаса'),
        ('Сосиски'),
        ('Кофе'),
        ('Чай'),
        ('Вода'),
        ('Лимонад'),
        ('Кефир'),
        ('Тушёнка'),
        ('Сгущёнка'),
        ('Шпроты'),
        ('Паштет'),
        ('Соленья'),
        ('Огурчики'),
        ('Кукуруза'),
        ('Перловка'),
        ('Киноа'),
        ('Арахис'),
        ('Миндаль'),
        ('Фундук'),
        ('Кешью'),
        ('Фисташки'),
        ('Семечки подсолнечные'),
        ('Семена мака'),
        ('Паста'),
        ('Хлопья'),
        ('Мюсли'),
        ('Мёд'),
        ('Картофель фри'),
        ('Замороженные овощи'),
        ('Холодец'),
        ('Винегрет'),
        ('Щи'),
        ('Борщ'),
        ('Солянка'),
        ('Окрошка'),
        ('Пельмени'),
        ('Вареники'),
        ('Сырники'),
        ('Оладьи'),
        ('Зефир'),
        ('Пряник'),
        ('Медовик'),
        ('Торт'),
        ('Печенье'),
        ('Шоколад'),
        ('Конфеты'),
        ('Чипсы'),
        ('Майонез'),
        ('Кетчуп'),
        ('Горчица'),
        ('Соевый соус'),
        ('Уксус'),
        ('Оливковое масло'),
        ('Маргарин'),
        ('Желе'),
        ('Варенье'),
        ('Икра'),
        ('Оливье'),
        ('Селёдка под шубой'),
        ('Корейская морковь'),
        ('Шашлык'),
        ('Манты'),
        ('Бородинский хлеб'),
        ('Ржаной хлеб'),
        ('Чёрный хлеб'),
        ('Паштет печёночный'),
        ('Рагу овощное'),
        ('Бекон'),
        ('Булочка с маком'),
        ('Соус'),
        ('Ряженка'),
        ('Пряности'),
        ('Паприка'),
        ('Кумин'),
        ('Базилик'),
        ('Орегано'),
        ('Корица'),
        ('Лавровый лист'),
        ('Розмарин')
    """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(op.f("uq_users_username"), "users", type_="unique")
    op.drop_column("users", "username")
    op.drop_table("profiles")
    op.drop_index(op.f("ix_products_name"), table_name="products")
    op.drop_table("products")
