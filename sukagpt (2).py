# -*- coding: utf-8 -*-
# meta developer: украл @svatoshgpt

# from .Hikka.hikka import loader, utils
from .. import loader, utils
import openai
import requests


@loader.tds
class GPT(loader.Module):
    """Задавайте вопросы sukaGPT"""
    strings = {"name": "sukaGPT"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            "OPENAI_API_KEY", None, "Ваш API ключ для OpenAI",
            "MODEL", "gpt-3.5-turbo", "Название модели для генерации ответов"
        )

    async def gptcmd(self, message):
        """Используйте .gpt <вопрос> или ответьте на сообщение"""
        
        if self.config["OPENAI_API_KEY"] is None:
            await utils.answer(message, "<b><emoji document_id=5210952531676504517>❌</emoji> Вы не указали API ключ для OpenAI. .cfg sukaGPT</b>")
            return
        api_key = self.config["OPENAI_API_KEY"]
        question = utils.get_args_raw(message)
        if not question:
            reply = await message.get_reply_message()
            if reply:
                question = reply.raw_text
            else:
                await utils.answer(message, "<b>Вы не задали вопрос.</b>")
                return

        prompt = [{"role": "user", "content": question}]

        await message.edit("<b><emoji document_id=5443038326535759644>💬</emoji> Генерирую ответ...</b>")
        try:
            client = openai.AsyncOpenAI(api_key=api_key)
            response = await client.chat.completions.create(
                model=self.config["MODEL"],
                messages=prompt
            )
            answer = response.choices[0].message.content
            await utils.answer(message, f"<b><emoji document_id=5452069934089641166>❓</emoji> Вопрос:</b> {question}\n<b>Ответ:</b> {answer}")
        except Exception as e:
            await utils.answer(message, f"<b><emoji document_id=5210952531676504517>❌</emoji> Произошла ошибка:</b> {e}")