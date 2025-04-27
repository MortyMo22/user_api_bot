# openai_api.py
import g4f

MODEL_PRIORITY = [
    'gpt-4',
    'gpt-4-32k',
    'gpt-4-turbo',
    'gpt-3.5-turbo',
    'gpt-3.5-turbo-16k',
    'gemini-pro',
    'claude-3-haiku',
    'claude-3-sonnet'
]

async def chat_with_g4f(user_message, preferred_model=None):
    models = MODEL_PRIORITY.copy()
    if preferred_model:
        models.remove(preferred_model)
        models.insert(0, preferred_model)

    for model_name in models:
        try:
            response = await g4f.ChatCompletion.create_async(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message}
                ],
            )
            return response
        except Exception as e:
            print(f"[WARN] Ошибка на модели {model_name}: {e}")
            continue
    raise Exception("⚠️ Все доступные модели недоступны в данный момент.")
