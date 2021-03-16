from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from random import shuffle, choice

answers = [
    'первый фильм',
    'фильм 2',
    'кино тринити',
    'золотой квартет'
]


class MovieQuiz(StatesGroup):
    set_question = State()
    get_answer = State()
    show_results = State()


async def set_question(message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    correct_answer = choice(answers)
    inner_answers = answers.copy()
    shuffle(inner_answers)

    for movie in inner_answers:
        keyboard.add(movie)

    await message.answer(f"угадай (правильный ответ {correct_answer})", reply_markup=keyboard)
    await state.update_data(correct_answer=correct_answer)
    await MovieQuiz.get_answer.set()


async def get_answer(message, state: FSMContext):
    stored_data = await state.get_data()

    user_answer = message.text.lower()

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
