# Добавьте FSInputFile в импорты в начале файла
from aiogram.types import Message, FSInputFile 

# ... (ваш предыдущий код до команд) ...

# ==== Команды бота ====
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        f"👋 <b>Бот для отслеживания GitLab</b>\n\n"
        f"📁 Проект: {project.name}\n"
        f"🌐 GitLab: {GITLAB_URL}\n\n"
        f"✅ Бот успешно запущен!\n"
        f"⏰ Проверка каждые 30 секунд\n"
        f"⚠️ Неактивность: более {INACTIVITY_DAYS} дней\n\n"
        f"Команды:\n"
        f"/status - статус бота\n"
        f"/members - активность участников\n"
        f"/inactive - неактивные участники",
        parse_mode="HTML"
    )
    # Отправка фото в конце
    await message.answer_photo(FSInputFile("prikol.jpg"))


@dp.message(Command("status"))
async def cmd_status(message: Message):
    await message.answer(
        f"✅ <b>Статус бота</b>\n\n"
        f"📁 Проект: {project.name}\n"
        f"📊 Проверка: каждые 30 сек\n"
        f"⏰ Неактивность: > {INACTIVITY_DAYS} дней\n"
        f"📝 Событий в кэше: {sum(len(v) for v in last_checked.values() if isinstance(v, dict))}",
        parse_mode="HTML"
    )
    # Отправка фото в конце
    await message.answer_photo(FSInputFile("prikol.png"))


@dp.message(Command("members"))
async def cmd_members(message: Message):
    try:
        if not members_activity:
            await message.answer("❌ Данные об активности еще собираются...")
            return

        response = "👥 <b>Активность участников:</b>\n\n"
        now = datetime.now()

        sorted_members = sorted(
            members_activity.items(),
            key=lambda x: x[1]['last_activity'] if x[1]['last_activity'] else datetime.min,
            reverse=True
        )

        for username, data in sorted_members[:10]:
            if data['last_activity']:
                days_ago = (now - data['last_activity']).days
                status = f"⚠️ Неактивен {days_ago} дн" if days_ago > INACTIVITY_DAYS else f"✅ Активен {days_ago} дн назад"
            else:
                status = "❌ Нет данных"

            response += f"👤 <b>{username}</b>\n{status}\n\n"

        await message.answer(response, parse_mode="HTML")
        # Отправка фото в конце
        await message.answer_photo(FSInputFile("prikol.png"))
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")


@dp.message(Command("inactive"))
async def cmd_inactive(message: Message):
    try:
        if not members_activity:
            await message.answer("❌ Данные об активности еще собираются...")
            return

        now = datetime.now()
        inactive_members = []

        for username, data in members_activity.items():
            if data['last_activity']:
                days_ago = (now - data['last_activity']).days
                if days_ago > INACTIVITY_DAYS:
                    inactive_members.append((username, days_ago))

        if inactive_members:
            response = f"⚠️ <b>Неактивные участники (> {INACTIVITY_DAYS} дн):</b>\n\n"
            for username, days in sorted(inactive_members, key=lambda x: x[1], reverse=True)[:10]:
                response += f"👤 {username} — {days} дн\n"
        else:
            response = "✅ Все участники активны!"

        await message.answer(response, parse_mode="HTML")
        # Отправка фото в конце
        await message.answer_photo(FSInputFile("prikol.png"))
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

# ... (остальной код без изменений) ...
