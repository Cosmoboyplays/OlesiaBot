# def decorator(func):
#     def wrapper(z):
#         print(11)
#         return func(z)
#     return wrapper
        

# @decorator
# def even_num(z: int) -> list:
#     x = -1 if z < 0 else 1    
#     print(*[i * x  for i in range(abs(z)) if i%2==0])

# even_num(-10)

# def decorator(func):

#     def inner(*args, **kwargs):
#         print('Start')
#         func(*args, **kwargs)
#         print('End')
#     return inner

# @decorator #text = decorator(text)
# def text(name, job, age):
#     print('Hello,', name, age, job)    

# text('Nikita', 'No job', 25 )

# print(text.__name__) 

import requests


api_url = 'http://numbersapi.com/43'

response = requests.get(api_url)   # Отправляем GET-запрос и сохраняем ответ в переменной response

if response.status_code == 200:    # Если код ответа на запрос - 200, то смотрим, что пришло в ответе
    print(response.text)
else:
    print(response.status_code) 