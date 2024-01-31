# Отримання результату від OpenAI та відправка його користувачу
async def get_chat_report(client, report, existing_report):

    if existing_report:
        context = (
            (
                "Ось попередні репорти по цій"
                f"локації від цього юзера {existing_report}"
            ),
        )
    else:
        context = "По цій локації ще не було звітів ще не було звітів"
    openai_response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Уяви що ти асистент який має аналізувати "
                "звіт та надавати репорт по данному звіту. "
                "Твої відповіді мають бути вичерпні "
                "та ти повинен НЕ задавати "
                "якихось уточнюючих запитань"
                "Також тобі можуть бути надіслані і минулі звіти"
                f"Ти їх повинен враховувати {context}",
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": report},
                ],
            },
        ],
    )
    return openai_response.choices[0].message.content.strip()
