import aiosqlite as sq

from config import DB_NAME


async def create_db():
    async with sq.connect(DB_NAME) as db:
        print("Database created!")

        await db.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            topic_id INTEGER
        )""")

        await db.commit()


async def insert_user(user_id, username, topic_id):
    async with sq.connect(DB_NAME) as db:
        await db.execute("INSERT OR REPLACE INTO users VALUES (?, ?, ?)", (user_id, username, topic_id))
        await db.commit()


async def get_user(user_id):
    async with sq.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = await cursor.fetchone()
        await db.commit()

        return user


async def update_topic_id(user_id, topic_id):
    async with sq.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET topic_id = ? WHERE user_id = ?", (topic_id, user_id))
        await db.commit()


async def get_questions_and_delete(question):
    async with sq.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT user_id FROM users WHERE topic_id = ?", (question,))
        user_id_row = await cursor.fetchone()

        # Проверка, найден ли пользователь
        if user_id_row is None:
            return None  # Возвращаем None, если пользователь не найден

        user_id = user_id_row[0]  # Извлекаем user_id из кортежа
        await db.commit()

        return user_id
