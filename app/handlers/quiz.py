from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from app.controller.kino import Kino

from random import shuffle, choice

from app.config_reader import load_config


config = load_config("config/bot.ini")
kino = Kino()
kino.set_api_token(config.tg_bot.kino_api)
kino.set_data()


class MovieQuiz(StatesGroup):
    set_question = State()
    get_answer = State()
    show_results = State()


async def set_question(message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    correct_id = kino.random_id
    correct_name = kino.data[correct_id]['nameRu']
    print(correct_name, correct_id, kino.data[correct_id]['year'])

    filtered_data = kino.filter_data(correct_id)
    answers = kino.get_options_list(correct_id, data=filtered_data)

    for answer in answers:
        keyboard.add(answer)

    img_url = kino.get_random_img(correct_id)
    photo_io = Kino.get_photo_by_url(img_url)
    await message.answer_photo(photo=photo_io,
                                #caption=correct_name,
                                reply_markup=keyboard)
#    await message.answer(f"{img_url}\n(правильный ответ {correct_name})", reply_markup=keyboard)

    await state.update_data(correct_answer=correct_name)
    await state.update_data(answers=answers)

    await MovieQuiz.get_answer.set()


async def get_answer(message, state: FSMContext):
    stored_data = await state.get_data()

    user_answer = message.text
    answers = stored_data['answers']

    if user_answer not in answers:
        await message.answer("нормально кнопки нажимай")
        return

    if stored_data['correct_answer'] == user_answer:
        await state.update_data(res = stored_data.get('res', 0) + 1)
        await message.answer("крос")
    else:
        await MovieQuiz.show_results.set()
        await show_results(message, state)




    await MovieQuiz.set_question.set()
    await set_question(message, state)


async def show_results(message, state: FSMContext):

    stored_data = await state.get_data()
    if 'res' in stored_data:
        await message.answer(f"наугадывал {stored_data['res']}")
    else:
        await message.answer(f"в этот раз без правильных ответов, додик")

    await message.answer("жми /random если чо",
                        reply_markup=types.ReplyKeyboardRemove())


    await state.finish()


def register_handlers_quiz(dp):
    dp.register_message_handler(set_question, commands='random', state='*')
    dp.register_message_handler(show_results, commands='stop', state='*')
    dp.register_message_handler(get_answer, state=MovieQuiz.get_answer)


    # dp.register_message_handler(wait_for_answer, state=MovieQuiz.wait_for_answer)
