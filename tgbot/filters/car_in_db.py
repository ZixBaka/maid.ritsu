import typing

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from tgbot.models.cars import Car


class CarInDB(BoundFilter):

    key = "car_in_db"

    def __init__(self, car_in_db: typing.Optional[bool] = key):
        self.car_in_db = car_in_db

    async def check(self, obj, *args):
        if self.car_in_db is None:
            return True
        print(self.car_in_db)
        session_maker = obj.bot.get('db')

        car_number: types.Message.text = obj.text

        car = await Car.get_car(session_maker, car_number)

        data = dict(car=car)
        print(car)
        if car is None:
            if self.car_in_db is True:
                print(".")
                return False
            else:
                print("..")
                return True

        if car is not None:
            if self.car_in_db is True:
                return data
            else:
                return False


