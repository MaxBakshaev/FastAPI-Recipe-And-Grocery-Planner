"""Changed calories_per_gram

Revision ID: 10aff5bf2197
Revises: c9de70a29627
Create Date: 2025-10-06 04:44:07.986290

"""

from typing import Sequence, Union

from alembic import op


revision: str = "10aff5bf2197"
down_revision: Union[str, Sequence[str], None] = "c9de70a29627"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        UPDATE products SET calories_per_gram = CASE name
            WHEN 'Яблоко' THEN 52.0 / 100
            WHEN 'Банан' THEN 89.0 / 100
            WHEN 'Апельсин' THEN 45.0 / 100
            WHEN 'Груша' THEN 42.0 / 100
            WHEN 'Киви' THEN 50.0 / 100
            WHEN 'Ананас' THEN 48.0 / 100
            WHEN 'Арбуз' THEN 40.0 / 100
            WHEN 'Дыня' THEN 45.0 / 100
            WHEN 'Виноград' THEN 70.0 / 100
            WHEN 'Клубника' THEN 36.0 / 100
            WHEN 'Малина' THEN 39.0 / 100
            WHEN 'Черника' THEN 44.0 / 100
            WHEN 'Смородина' THEN 43.0 / 100
            WHEN 'Персик' THEN 45.0 / 100
            WHEN 'Нектарин' THEN 45.0 / 100
            WHEN 'Манго' THEN 60.0 / 100
            WHEN 'Папайя' THEN 43.0 / 100
            WHEN 'Лимон' THEN 18.0 / 100
            WHEN 'Лайм' THEN 18.0 / 100
            WHEN 'Авокадо' THEN 160.0 / 100
            WHEN 'Картофель' THEN 60.0 / 100
            WHEN 'Морковь' THEN 33.0 / 100
            WHEN 'Свёкла' THEN 43.0 / 100
            WHEN 'Томат' THEN 23.0 / 100
            WHEN 'Огурец' THEN 15.0 / 100
            WHEN 'Капуста' THEN 23.0 / 100
            WHEN 'Брокколи' THEN 34.0 / 100
            WHEN 'Цветная капуста' THEN 18.0 / 100
            WHEN 'Лук' THEN 43.0 / 100
            WHEN 'Чеснок' THEN 149.0 / 100
            WHEN 'Шпинат' THEN 23.0 / 100
            WHEN 'Петрушка' THEN 36.0 / 100
            WHEN 'Укроп' THEN 43.0 / 100
            WHEN 'Сельдерей' THEN 16.0 / 100
            WHEN 'Фасоль' THEN 329.0 / 100
            WHEN 'Горох' THEN 303.0 / 100
            WHEN 'Чечевица' THEN 310.0 / 100
            WHEN 'Рис' THEN 338.0 / 100
            WHEN 'Гречка' THEN 329.0 / 100
            WHEN 'Овсянка' THEN 374.0 / 100
            WHEN 'Пшено' THEN 348.0 / 100
            WHEN 'Макароны' THEN 337.0 / 100
            WHEN 'Хлеб' THEN 231.0 / 100
            WHEN 'Булка' THEN 300.0 / 100
            WHEN 'Мука' THEN 346.0 / 100
            WHEN 'Сахар' THEN 387.0 / 100
            WHEN 'Соль' THEN 0.0
            WHEN 'Перец чёрный' THEN 255.0 / 100
            WHEN 'Молоко' THEN 52.0 / 100
            WHEN 'Сыр' THEN 350.0 / 100
            WHEN 'Творог' THEN 101.0 / 100
            WHEN 'Сметана' THEN 160.0 / 100
            WHEN 'Йогурт' THEN 51.0 / 100
            WHEN 'Масло сливочное' THEN 717.0 / 100
            WHEN 'Масло растительное' THEN 884.0 / 100
            WHEN 'Курица' THEN 167.0 / 100
            WHEN 'Говядина' THEN 187.0 / 100
            WHEN 'Свинина' THEN 316.0 / 100
            WHEN 'Рыба' THEN 59.0 / 100
            WHEN 'Яйцо' THEN 157.0 / 100
            WHEN 'Колбаса' THEN 255.0 / 100
            WHEN 'Сосиски' THEN 225.0 / 100
            WHEN 'Кофе' THEN 0.0
            WHEN 'Чай' THEN 0.0
            WHEN 'Вода' THEN 0.0
            WHEN 'Лимонад' THEN 40.0 / 100
            WHEN 'Кефир' THEN 56.0 / 100
            WHEN 'Тушёнка' THEN 200.0 / 100
            WHEN 'Сгущёнка' THEN 320.0 / 100
            WHEN 'Шпроты' THEN 253.0 / 100
            WHEN 'Паштет' THEN 300.0 / 100
            WHEN 'Соленья' THEN 19.0 / 100
            WHEN 'Огурчики' THEN 15.0 / 100
            WHEN 'Кукуруза' THEN 96.0 / 100
            WHEN 'Перловка' THEN 320.0 / 100
            WHEN 'Киноа' THEN 368.0 / 100
            WHEN 'Арахис' THEN 548.0 / 100
            WHEN 'Миндаль' THEN 645.0 / 100
            WHEN 'Фундук' THEN 704.0 / 100
            WHEN 'Кешью' THEN 643.0 / 100
            WHEN 'Фисташки' THEN 572.0 / 100
            WHEN 'Семечки подсолнечные' THEN 578.0 / 100
            WHEN 'Семена мака' THEN 525.0 / 100
            WHEN 'Паста' THEN 348.0 / 100
            WHEN 'Хлопья' THEN 308.0 / 100
            WHEN 'Мюсли' THEN 380.0 / 100
            WHEN 'Мёд' THEN 312.0 / 100
            WHEN 'Картофель фри' THEN 312.0 / 100
            WHEN 'Замороженные овощи' THEN 25.0 / 100
            WHEN 'Холодец' THEN 150.0 / 100
            WHEN 'Винегрет' THEN 120.0 / 100
            WHEN 'Щи' THEN 25.0 / 100
            WHEN 'Борщ' THEN 58.0 / 100
            WHEN 'Солянка' THEN 60.0 / 100
            WHEN 'Окрошка' THEN 40.0 / 100
            WHEN 'Пельмени' THEN 250.0 / 100
            WHEN 'Вареники' THEN 230.0 / 100
            WHEN 'Сырники' THEN 220.0 / 100
            WHEN 'Оладьи' THEN 300.0 / 100
            WHEN 'Зефир' THEN 295.0 / 100
            WHEN 'Пряник' THEN 351.0 / 100
            WHEN 'Медовик' THEN 400.0 / 100
            WHEN 'Торт' THEN 400.0 / 100
            WHEN 'Печенье' THEN 430.0 / 100
            WHEN 'Шоколад' THEN 546.0 / 100
            WHEN 'Конфеты' THEN 576.0 / 100
            WHEN 'Чипсы' THEN 536.0 / 100
            WHEN 'Майонез' THEN 665.0 / 100
            WHEN 'Кетчуп' THEN 112.0 / 100
            WHEN 'Горчица' THEN 139.0 / 100
            WHEN 'Соевый соус' THEN 53.0 / 100
            WHEN 'Уксус' THEN 0.0
            WHEN 'Оливковое масло' THEN 884.0 / 100
            WHEN 'Маргарин' THEN 717.0 / 100
            WHEN 'Желе' THEN 40.0 / 100
            WHEN 'Варенье' THEN 286.0 / 100
            WHEN 'Икра' THEN 203.0 / 100
            WHEN 'Оливье' THEN 150.0 / 100
            WHEN 'Селёдка под шубой' THEN 200.0 / 100
            WHEN 'Корейская морковь' THEN 150.0 / 100
            WHEN 'Шашлык' THEN 240.0 / 100
            WHEN 'Манты' THEN 220.0 / 100
            WHEN 'Бородинский хлеб' THEN 219.0 / 100
            WHEN 'Ржаной хлеб' THEN 183.0 / 100
            WHEN 'Чёрный хлеб' THEN 231.0 / 100
            WHEN 'Паштет печёночный' THEN 300.0 / 100
            WHEN 'Рагу овощное' THEN 50.0 / 100
            WHEN 'Бекон' THEN 541.0 / 100
            WHEN 'Булочка с маком' THEN 300.0 / 100
            WHEN 'Соус' THEN 120.0 / 100
            WHEN 'Ряженка' THEN 56.0 / 100
            WHEN 'Пряности' THEN 0.0
            WHEN 'Паприка' THEN 289.0 / 100
            WHEN 'Кумин' THEN 375.0 / 100
            WHEN 'Базилик' THEN 22.0 / 100
            WHEN 'Орегано' THEN 43.0 / 100
            WHEN 'Корица' THEN 247.0 / 100
            WHEN 'Лавровый лист' THEN 313.0 / 100
            WHEN 'Розмарин' THEN 331.0 / 100
            ELSE calories_per_gram
        END
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
