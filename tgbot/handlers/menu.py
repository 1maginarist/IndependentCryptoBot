from aiogram import types, Dispatcher
from tgbot.keyboards.inline import currencies
from tgbot.keyboards.callback_datas import currencies_callback
import asyncio
import datetime
import time
import aiohttp
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import requests
from dataclasses import dataclass

genesis_dates = {'bitcoin': "2009-01-03", 'ethereum': "2015-07-30", 'binancecoin': "2017-07-08", 'ripple': '2013-09-01',
                 'cardano': '2017-10-23', 'matic-network': '2019-05-03', 'solana': '2020-04-27',
                 'polkadot': '2020-08-24',
                 'litecoin': '2011-10-08', 'tron': '2017-08-28', 'shiba-inu': '2020-08-10'}

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


@dataclass
class Token:
	id: str
	date_start: int
	date_end: int


@dataclass
class Dataset:
	token_independent: Token
	token_dependent: Token


async def create_token(coin_id: str) -> Dataset:
	return Dataset(
		token_independent = Token(
			id = "bitcoin",
			date_start = await to_timestamp(genesis_dates[coin_id]),
			date_end = await get_date()
		),
		token_dependent = Token(
			id = coin_id,
			date_start = await to_timestamp(genesis_dates[coin_id]),
			date_end = await get_date()
		)
	)

async def get_date():
	yesterday = datetime.date.today() - datetime.timedelta(days=1)
	return int(time.mktime(yesterday.timetuple()))

async def to_timestamp(date):
	date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
	timestamp = int(date_obj.timestamp())
	return timestamp


async def get_response(token: Token):
	endpoint = f"https://coingecko.p.rapidapi.com/coins/{token.id}/market_chart/range"

	params = {"from":f"{token.date_start}",
			  "vs_currency":"usd",
			  "to":f"{token.date_end}"}

	headers = {
		"content-type": "application/octet-stream",
		"X-RapidAPI-Key": "84a83de9d5msh1d1244df6174706p10730ajsn04d81494b440",
		"X-RapidAPI-Host": "coingecko.p.rapidapi.com"
	}

	async with aiohttp.ClientSession() as session:
		async with session.get(endpoint, headers=headers, params=params) as response:
			response_json = await response.json()
			return response_json



async def form_dataset(data: dict):
	df_price = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
	df_price['timestamp'] = pd.to_datetime(df_price['timestamp'], unit='ms')
	df_price.set_index('timestamp', inplace=True)
	df_price['price'] = df_price['price'].astype(float)
	return df_price


async def main(data):
	dataset = await create_token(data['coin_id'])
	independent = await get_response(dataset.token_independent)
	dependent = await get_response(dataset.token_dependent)

	df_independent = await form_dataset(independent)
	df_dependent = await form_dataset(dependent)

	df_combined = pd.concat([df_independent, df_dependent], axis=1).dropna()
	df_combined.columns = ['independent_price', 'dependent_price']

	df_pct_change = df_combined.pct_change().dropna()

	print(df_pct_change)

	y = df_pct_change.iloc[:, 0]
	X = df_pct_change.iloc[:, 1:].values.reshape(-1, 1)

	reg = LinearRegression().fit(X, y)

	values = [reg.coef_, reg.score(X, y)]
	return values

async def menu(message: types.Message):
	await message.answer("Choose cryptocurrency", reply_markup=currencies)


async def count_regression(call: types.CallbackQuery, callback_data: dict):
	await call.answer()
	coin_id = callback_data.get("id")

	data_dict = {'coin_id': coin_id}

	values = await main(data_dict)

	await call.message.answer(f"{coin_id} price changes for {values[0][0]}% for every 1% of bitcoin's price change\n"
							  f"{values[1]}% price movements can be explained by bitcoin price movement")


def register_menu(dp: Dispatcher):
	dp.register_message_handler(menu, commands=["menu"])
	dp.register_callback_query_handler(count_regression, currencies_callback.filter(type="currency"))
