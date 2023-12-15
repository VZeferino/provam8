import io
import gradio as gr
from langchain.llms import Ollama
import httpx
from pydub import AudioSegment
from pydub.playback import play

class ChatbotDemo:
    def __init__(self):
        self.history = []
        self.ollama = Ollama(base_url='http://localhost:11434', model="orca-mini")

    async def generate_response(self, prompt):
        context = "\n".join([h[1] for h in self.history])
        full_prompt = context + "\nQuestion: " + prompt
        response = self.ollama(full_prompt)
        self.history.append((prompt, response))
        await self.text_to_speech(response)
        return [(prompt, response)]

    async def text_to_speech(self, response):
        try:
            with httpx.Client() as client:
                path = client.post('http://localhost:8000/tts/', json={'text': response, 'lang': 'en'}).content
                song = AudioSegment.from_file(io.BytesIO(path), format="mp3")
                play(song)
        except httpx.RequestError as e:
            print(f"Erro: {e}")

def main():
    demo = ChatbotDemo()
    with gr.Blocks() as demo_interface:
        gr.Markdown("### Friendly friend")
        chatbot = gr.Chatbot()
        msg = gr.Textbox(label="Your Question")
        msg.submit(demo.generate_response, inputs=msg, outputs=chatbot)

    demo_interface.launch()

if __name__ == "__main__":
    main()



