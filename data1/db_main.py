import aiosqlite
import asyncio
from data1.shara import *

path = 'C:\\Users\\admin\\PycharmProjects\\monefy\\data1\\monefy.db'


async def select_user_id(user):
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute("SELECT id FROM users WHERE telegram_id = ?", (user,))
        result = (await cursor.fetchone())[0]
        if result:
            return result
        else:
            return None


async def select_categories_id(user, categorie):
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute("SELECT id FROM categories WHERE users_id = ? AND categorie = ?",
                             (await select_user_id(user), categorie))
        result = await cursor.fetchone()
        return result[0]


# print(asyncio.get_event_loop().run_until_complete(select_user_id('428392590')))


async def db_add_user(user) -> None:
    async with aiosqlite.connect(path) as db:
        await db.execute(f"INSERT OR IGNORE INTO users (telegram_id) VALUES (?)", (user,))
        await db.commit()


async def db_add_categories(user) -> None:
    async with aiosqlite.connect(path) as db:
        user_id = await select_user_id(user)
        values = []
        for i in categories:
            values.append((user_id, i))
        await db.executemany("INSERT OR IGNORE INTO categories (users_id, categorie) VALUES (?, ?)", values)
        await db.commit()


async def db_add_categorie(user, categorie):
    async with aiosqlite.connect(path) as db:
        user_id = await select_user_id(user)
        existing_category = await db.execute(
            "SELECT categorie FROM categories WHERE users_id = ? AND categorie = ?",
            (user_id, categorie,)
        )
        existing_category = await existing_category.fetchone()
        if existing_category:
            return f"Категория '{categorie}' уже существует"
        else:
            await db.execute(
                "INSERT OR IGNORE INTO categories (users_id, categorie) VALUES (?, ?)",
                (user_id, categorie,)
            )
            await db.commit()


async def db_select_categories(user):
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute("SELECT categorie FROM categories WHERE users_id = ?", (await select_user_id(user),))
        return [i[0] for i in await cursor.fetchall()]


async def db_add_record(item):
    async with aiosqlite.connect(path) as db:
        await db.execute(f"INSERT INTO records (users_id, categories_id, record, text) VALUES (?, ?, ?, ?)",
                         (await select_user_id(item['telegarm_id']),
                          await select_categories_id(str(item['telegarm_id']), item['categories']),
                          item['record'],
                          item['text']
                          ))
        await db.commit()


async def db_select_spending(user, days: str, s_p=''):
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        tuple1 = {
            'today': "SELECT record FROM records WHERE DATETIME(date) >= DATE('now') AND DATETIME(date) < "
                     "DATE('now', '+1 day') AND users_id = ?",
            'last_7_days': "SELECT strftime('%Y-%m-%d', date) AS days, "
                           "SUM(record) FROM records WHERE DATETIME(date) >= "
                           "DATE('now', '-6 days') AND DATETIME(date) < DATE('now', '+1 day') AND users_id = ? "
                           "GROUP BY days ORDER BY days DESC",
            'summary_by_month': "SELECT strftime('%Y-%m', date) AS month, SUM(record) AS total FROM records "
                                "WHERE users_id = ? GROUP BY month ORDER BY month DESC",
            'specific_date': "SELECT record FROM records WHERE STRFTIME('%d.%m.%Y', date) = ? "
                             "AND users_id = ?"}
        if days == 'specific_date':
            await cursor.execute(tuple1[days], (s_p, await select_user_id(user)))
            return sum([i[0] for i in await cursor.fetchall()])

        await cursor.execute(tuple1[days], (await select_user_id(user),))
        if days == 'summary_by_month':
            return [(f"{months_dict[i[0].split('-')[-1]]} {i[0].split('-')[0]}",
                     i[-1]) for i in await cursor.fetchall()]
        elif days == 'last_7_days':
            return [('.'.join(i[0].split('-')[::-1]), i[-1]) for i in await cursor.fetchall()]
        elif days == 'today':
            return sum([i[0] for i in await cursor.fetchall()])


# print(asyncio.get_event_loop().run_until_complete(db_select_spending(428392590, days='today')))


async def conversion_to_category(user, category, id_or_categorie):
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        tuple1 = {
            'categorie': "SELECT categorie FROM categories WHERE users_id = ? AND id = ?",
            'id_categories': "SELECT id FROM categories WHERE users_id = ? AND categorie = ?"
        }
        await cursor.execute(tuple1[id_or_categorie], (await select_user_id(user), category))
        return [i[0] for i in await cursor.fetchall()][0]
# print(asyncio.get_event_loop().run_until_complete(conversion_to_category(428392590, 'Еда🍔', 'id_categories')))


async def db_select_spending_by_group(user, days: str):     # for keyboards
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        tuple1 = {
            'today': "SELECT categories_id, SUM(record) as total_spending FROM records "
                     "WHERE DATETIME(date) >= DATE('now') AND "
                     "DATETIME(date) < DATE('now', '+1 day') AND users_id = ? "
                     "GROUP BY categories_id",
            'last_7_days': "SELECT categories_id, SUM(record) as total_spending FROM records "
                           "WHERE DATETIME(date) >= DATE('now', '-6 days') AND DATETIME(date) < DATE('now', '+1 day') "
                           "AND users_id = ? GROUP BY categories_id"
        }
        await cursor.execute(tuple1[days], (await select_user_id(user),))
        list1 = [[category, value] for category, value in await cursor.fetchall()]
        for i in range(len(list1)):
            list1[i][0] = await conversion_to_category(user, list1[i][0], 'categorie')
        return list1


# async def db_select_spending_specific_date(user, date):
#     async with aiosqlite.connect(path) as db:
#         cursor = await db.cursor()
#         await cursor.execute("SELECT categories_id, SUM(record) as total_spending FROM records "
#                              "WHERE users_id = ? AND STRFTIME('%d.%m.%Y', date) = ? "
#                              "GROUP BY categories_id", (await select_user_id(user), date))
#         list1 = [[category, value] for category, value in await cursor.fetchall()]
#         for i in range(len(list1)):
#             list1[i][0] = await conversion_to_category(user, list1[i][0])
#         return list1

async def db_select_spending_specific_categorie_last_7_days(user_id, categorie):
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        l = "SELECT id, record, text, date FROM records WHERE DATETIME(date) >= DATE('now', '-6 days') AND" \
            " DATETIME(date) < DATE('now', '+1 day') AND users_id = ? AND categories_id = ?"
        await cursor.execute(l, (await select_user_id(user_id),
                                 await conversion_to_category(user_id, categorie, 'id_categories'),))
        return await cursor.fetchall()
# print(asyncio.get_event_loop().run_until_complete(db_select_spending_specific_categorie_last_7_days(428392590, 'Связь📡')))


async def db_select_currency(user):
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute("SELECT currency FROM users WHERE telegram_id = ?", (user,))
        return [i[0] for i in await cursor.fetchall()][0]


async def db_currency_setting(currency, user):
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute("UPDATE users SET currency = ? WHERE telegram_id = ?", (currency, user))
        await db.commit()


async def create_table():
    async with aiosqlite.connect(path) as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    users_id INTEGER,
    categorie TEXT,
    UNIQUE (users_id, categorie));""")
        await db.commit()


