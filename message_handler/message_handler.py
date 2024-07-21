from aiogram import Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from BotCommand.command import set_commands
from get_text.get_text import *
from states.states import Form
from exchange_rates.exchange_rates import *

app_router = Router(name=__name__)


@app_router.message(CommandStart())
async def command_start_handler(message: Message, bot: Bot) -> None:
    await set_commands(bot)
    await message.answer(text=await get_first_text(message.from_user.username), parse_mode='markdown')


@app_router.message(Command('exchange'))
async def exchange(message: Message, state: FSMContext):
    await state.set_state(Form.currency)
    await message.answer(await get_command_exchange(), parse_mode='markdown')


@app_router.message(Form.currency)
async def process_currency(message: Message, state: FSMContext):
    try:
        command_parts = message.text.split()
        if len(command_parts) != 3:
            await message.answer(await get_command_exchange(), parse_mode='markdown')
            return

        from_currency, to_currency, amount_str = command_parts
        amount = float(amount_str)

        from_rate = float(r.get(from_currency))
        to_rate = float(r.get(to_currency))

        if from_rate and to_rate:
            result = (amount / from_rate) * to_rate
            await message.answer(f'{amount} {from_currency} = {result:.2f} {to_currency}')
        else:
            await message.answer(await error_message())
    except ValueError as ve:
        await message.answer(await value_error_message())
    except Exception as e:
        await message.answer(await command_error(), parse_mode='markdown')
    finally:
        await state.clear()


@app_router.message(Command('rates'))
async def cmd_rates(message: Message):
    requested_currencies = message.text.split()[1:]

    if not requested_currencies:
        await message.answer(await error_rates(), parse_mode='markdown')
        return

    rates = {}
    for currency in requested_currencies:
        rate = r.get(currency)
        if rate:
            rates[currency] = rate

    if rates:
        rates_message = '\n'.join([f'{currency}: {rate}' for currency, rate in rates.items()])
        await message.answer(await get_rates(rates_message), parse_mode='markdown')
    else:
        await message.answer(await rate_error(), parse_mode='markdown')
