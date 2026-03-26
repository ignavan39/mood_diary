from presentation.vk.keyboards.main import ButtonColor, VkKeyboard


def kb_mood_select() -> str:
    keyboard = VkKeyboard(inline=False)

    for i in range(10, 7, -1):
        keyboard.add_text(
            label=f"😌 {i}",
            color=ButtonColor.POSITIVE,
        )
    keyboard.row()

    for i in range(7, 4, -1):
        keyboard.add_text(
            label=f"🙂 {i}",
            color=ButtonColor.PRIMARY,
        )
    keyboard.row()

    for i in range(4, 0, -1):
        keyboard.add_text(
            label=f"😔 {i}",
            color=ButtonColor.NEGATIVE if i <= 2 else ButtonColor.SECONDARY,
        )
    keyboard.row()

    keyboard.add_text("❌ Отмена", color=ButtonColor.NEGATIVE)

    return keyboard.to_json()
