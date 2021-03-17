from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter

async def cmd_start(message, state: FSMContext):
    await state.finish()
    await message.answer(
        "нажимайте /random пожалуйста",
        reply_markup=types.ReplyKeyboardRemove()
    )


async def cmd_cancel(message, state: FSMContext):
    await state.finish()
    await message.answer(
        "отмена отмена",
        reply_markup=types.ReplyKeyboardRemove()
    )


async def secret_command(message):
    await anwswer("дарова отец")


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    # dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    # dp.register_message_handler(
    #     cmd_cancel,Text(equals="отмена", ignore_case=True), state="*"
    # )
    # dp.register_message_handler(
    #     secret_command, IDFilter(user_id=admin_id), commands="дарова"
    # )
