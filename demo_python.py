#def say_something(number: int, word: str) -> str:
 #   word = word.capitalize()
  #  return word * number

#class User:
 #   def __init__(self, user_id, name, age, email):
  #      self.user_id = user_id
   #     self.name = name
    #    self.age = age
     #   self.email = email

import asyncio
import time


async def send_mail(num):
    print(f'Улетело сообщение {num}')
    await asyncio.sleep(1)  # Имитация отправки сообщения по сети
    print(f'Сообщение {num} доставлено')


async def main():
    tasks = [send_mail(1) for i in range(1000)]
    await asyncio.gather(*tasks)


start_time = time.time()
asyncio.run(main())
print(f'Время выполнения программы: {time.time() - start_time} с')