import os
from aiogram.types import Message, File


class PhotoHandler:
    PHOTO_STORAGE_PATH = os.path.join("photo_handler", "media")

    def ensure_media_folder_exists(self):
        if not os.path.exists(self.PHOTO_STORAGE_PATH):
            os.makedirs(self.PHOTO_STORAGE_PATH)

    # Зберегти файл
    async def save_photo_data(self, photo_message: Message, bot) -> str:
        self.ensure_media_folder_exists()
        photo_file = await bot.get_file(photo_message.photo[-1].file_id)

        photo_path = os.path.join(
            self.PHOTO_STORAGE_PATH, f"{photo_message.photo[-1].file_id}.jpg"
        )
        await photo_file.download(photo_path)
        return photo_message.photo[-1].file_id

    # Повернути URL фото
    async def get_photo_url(self, photo_file_id: str) -> File:
        photo_file = await self.bot.get_file(photo_file_id)
        return photo_file.file_path


photo_handler = PhotoHandler()
