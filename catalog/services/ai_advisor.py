import os
import requests


def get_advice(product, question):
    api_key = os.getenv('DEEPSEEK_API_KEY')

    # Если ключа нет, отдаем заглушку
    if not api_key:
        return f"Здравствуйте! Это демо-режим AI. Отличный выбор — {product.name} за {product.price} руб. Он идеально подходит для ваших задач!"

    # Если ключ есть, идем в DeepSeek
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system",
                 "content": f"Ты консультант магазина электроники. Товар: {product.name}. Цена: {product.price}. Описание: {product.description}. Отвечай кратко и вежливо."},
                {"role": "user", "content": question}
            ]
        }
        response = requests.post('https://api.deepseek.com/chat/completions', headers=headers, json=data, timeout=15)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Извините, AI временно недоступен. Но я могу сказать, что {product.name} — отличный выбор!"