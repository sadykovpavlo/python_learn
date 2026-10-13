import asyncio
import time


async def return_name(name: str):
    return f"Hello {name.title()}"


async def return_name_sleep(name, delay):
    await asyncio.sleep(delay)
    return f"Hello {name.title()}"


async def main_sbs():
    time_start = time.perf_counter()
    await return_name_sleep("pasha", 2)
    await return_name_sleep("igor", 2)
    time_stop = time.perf_counter()
    return f'main_sbs : {time_stop - time_start}'

async def main_all():
    time_start = time.perf_counter()
    await asyncio.gather(return_name_sleep("pasha", 2), return_name_sleep("igor", 2))
    time_stop = time.perf_counter()
    return f'main_all : {time_stop - time_start}'

async def validate_age(age: int):
    if age < 0:
        raise ValueError("Age cant be less than 0")
    await asyncio.sleep(0.1)
    return age

if __name__ == '__main__':

    print(asyncio.run(main_sbs()))
    print(asyncio.run(main_all()))