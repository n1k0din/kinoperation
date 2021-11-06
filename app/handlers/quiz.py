import io
from dataclasses import dataclass
from random import shuffle, choice

import requests
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from app.config_reader import load_config


config = load_config("config/bot.ini")


@dataclass
class Question:
    options: list[str]
    frame_url: str
    correct_answer: str


def get_question():
    url = 'https://kekinoapi.eu.pythonanywhere.com/question'
    response = requests.get(url)
    response.raise_for_status()

    question = response.json()

    return Question(question['options'], question['frame_url'], question['correct'])


def get_photo_by_url(url):
    response = requests.get(url)
    photo = io.BytesIO(response.content)
    photo.name = 'img.jpg'

    return photo


class MovieQuiz(StatesGroup):
    set_question = State()
    get_answer = State()
    show_results = State()


async def set_question(message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    question = get_question()

    for answer in question.options:
        keyboard.add(answer)

    if not question.frame_url:
        return

    photo_io = get_photo_by_url(question.frame_url)
    await message.answer_photo(photo=photo_io, reply_markup=keyboard)

    await state.update_data(correct_answer=question.correct_answer)
    await state.update_data(answers=question.options)

    await MovieQuiz.get_answer.set()


async def get_answer(message, state: FSMContext):
    # отклик на правильный ответ
    correct_response = ("хорош", "ага", "крос", "чот изи", "верняк", "по кайфу")

    stored_data = await state.get_data()

    user_answer = message.text
    answers = stored_data['answers']

    if user_answer not in answers:
        await message.answer("нормально кнопки нажимай")
        return

    if stored_data['correct_answer'] == user_answer:
        await state.update_data(res=stored_data.get('res', 0) + 1)
        await message.answer(choice(correct_response))
    else:
        await MovieQuiz.show_results.set()
        await show_results(message, state)

    await MovieQuiz.set_question.set()
    await set_question(message, state)


async def show_results(message, state: FSMContext):

    stored_data = await state.get_data()
    if 'correct_answer' in stored_data:
        await message.answer(f"зайка, правильный ответ был {stored_data['correct_answer']}")

    if 'res' in stored_data:
        await message.answer(f"угадано: {stored_data['res']}")
    else:
        await message.answer(f"в этот раз без правильных ответов, додик")

    await message.answer("жми /random если чо", reply_markup=types.ReplyKeyboardRemove())

    await state.finish()


def register_handlers_quiz(dp):
    dp.register_message_handler(set_question, commands='random', state='*')
    dp.register_message_handler(show_results, commands='stop', state='*')
    dp.register_message_handler(get_answer, state=MovieQuiz.get_answer)