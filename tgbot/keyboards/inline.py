from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from tgbot.keyboards.callback_datas import currencies_callback


currencies = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="ETH", callback_data=currencies_callback.new(type="currency", id="ethereum")),
        InlineKeyboardButton(text="BNB", callback_data=currencies_callback.new(type="currency", id="binancecoin")),
    ],
    [
        InlineKeyboardButton(text="XRP", callback_data=currencies_callback.new(type="currency", id="ripple")),
        InlineKeyboardButton(text="ADA", callback_data=currencies_callback.new(type="currency", id="cardano")),
    ],
    [
        InlineKeyboardButton(text="MATIC", callback_data=currencies_callback.new(type="currency", id="matic-network")),
        InlineKeyboardButton(text="SOL", callback_data=currencies_callback.new(type="currency", id="solana")),
    ],
    [
        InlineKeyboardButton(text="DOT", callback_data=currencies_callback.new(type="currency", id="polkadot")),
        InlineKeyboardButton(text="LTC", callback_data=currencies_callback.new(type="currency", id="litecoin")),
    ],
    [
        InlineKeyboardButton(text="TRX", callback_data=currencies_callback.new(type="currency", id="tron")),
        InlineKeyboardButton(text="SHIB", callback_data=currencies_callback.new(type="currency", id="shiba-inu")),
    ]
])