import os

import yfinance as yf
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
	await update.message.reply_text(
		"欢迎使用股票机器人！\n"
		"使用 /price 股票代码 查询股价\n"
		"例如：/price AAPL"
	)


async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
	if not context.args:
		await update.message.reply_text("请加上股票代码，例如：/price AAPL")
		return

	symbol = context.args[0].upper()
	try:
		ticker = yf.Ticker(symbol)
		info = ticker.info
		price = info.get("currentPrice") or info.get("regularMarketPrice")
		name = info.get("shortName", symbol)

		if price:
			await update.message.reply_text(f"{name} ({symbol})\n当前价格：${price}")
		else:
			await update.message.reply_text(f"未找到 {symbol} 的价格信息")
	except Exception as e:
		await update.message.reply_text(f"查询失败：{str(e)}")


def main():
	app = Application.builder().token(TOKEN).build()

	app.add_handler(CommandHandler("start", start))
	app.add_handler(CommandHandler("price", get_price))

	print("股票机器人已启动...")
	app.run_polling()


if __name__ == "__main__":
	main()
