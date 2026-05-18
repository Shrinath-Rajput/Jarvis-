import ollama


def ask_ai(prompt):

    try:
        response = ollama.chat(
            model='tinyllama',
            messages=[
                {
                    'role': 'system',
                    'content': '''
You are PREMEX AI.

You are an advanced autonomous AI assistant like Jarvis.

You can:
- understand natural language
- control computer
- create folders
- write code
- open apps
- automate tasks
- explain things
- help user intelligently

Always reply short and smart.
'''
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )

        return response['message']['content']

    except Exception as e:
        return f"AI Error: {str(e)}"