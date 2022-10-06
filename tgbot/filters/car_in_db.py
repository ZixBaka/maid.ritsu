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
        session_maker = obj.bot.get('db')

        car_number: types.Message.text = obj.text
<<<<<<< HEAD
        car = await Car.get_active_car(session_maker, car_number)
=======
        car = await Car.get_active_car(session_maker, car_number.upper())
>>>>>>> pr/11

        data = dict(car=car)
        if car is None:
            if self.car_in_db is True:
                return False
            else:
                return True

        if car is not None:
            if self.car_in_db is True:
                return data
            else:
                return False


class HasCar(BoundFilter):

    key = "has_car"

    def __init__(self, has_car: typing.Optional[bool] = key):
        self.has_car = has_car

    async def check(self, obj, *args):
        if self.has_car is None:
            return True
        elif self.has_car is True:
            session_maker = obj.bot.get('db')

            car_owner: types.Message.from_user = obj.from_user
            car = await Car.get_car_by_tg(session_maker, tg_id=car_owner.id)
            if car is None:
                return False
            data = dict(car=car)
            return data
