import requests

class BaseLLM:
    """
    Base class for language models.
    """
    def __init__(self, endpoint, token):
        self.endpoint = endpoint
        self.token = token
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

    def run(self, options, callback=None, fallback=None):
        raise NotImplementedError("The 'run' method must be implemented in subclasses.")


class TextToText(BaseLLM):
    """
    Text-to-text language model.
    """
    def run(self, options, callback=None, fallback=None):
        try:
            response = requests.post(self.endpoint, headers=self.headers, json=options)
            response.raise_for_status()

            if options.get("stream", False):
                # Stream response handling (if supported)
                result = ""
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        decoded_chunk = chunk.decode("utf-8")
                        result += decoded_chunk
                        if callback:
                            callback(decoded_chunk)
                return result
            else:
                data = response.json()
                if callback:
                    callback(data)
                return data

        except requests.exceptions.RequestException as e:
            if fallback:
                fallback(str(e))


class TextToSpeech(BaseLLM):
    """
    Text-to-speech language model.
    """
    def run(self, options, callback=None, fallback=None):
        try:
            response = requests.post(self.endpoint, headers=self.headers, json=options)
            response.raise_for_status()
            audio_data = response.content  # Handle audio as binary content
            if callback:
                callback(audio_data)
            return audio_data

        except requests.exceptions.RequestException as e:
            if fallback:
                fallback(str(e))


class SpeechToText(BaseLLM):
    """
    Speech-to-text language model.
    """
    def run(self, options, callback=None, fallback=None):
        try:
            files = {"file": (options["file"].name, options["file"], "audio/wav")}
            response = requests.post(self.endpoint, headers=self.headers, files=files, data=options)
            response.raise_for_status()
            data = response.json()
            if callback:
                callback(data)
            return data

        except requests.exceptions.RequestException as e:
            if fallback:
                fallback(str(e))


class ImageToText(BaseLLM):
    """
    Image-to-text language model.
    """
    def run(self, options, callback=None, fallback=None):
        try:
            files = {"file": (options["file"].name, options["file"], "image/png")}
            response = requests.post(self.endpoint, headers=self.headers, files=files, data=options)
            response.raise_for_status()
            data = response.json()
            if callback:
                callback(data)
            return data

        except requests.exceptions.RequestException as e:
            if fallback:
                fallback(str(e))


class TextToImage(BaseLLM):
    """
    Text-to-image language model.
    """
    def run(self, options, callback=None, fallback=None):
        try:
            response = requests.post(self.endpoint, headers=self.headers, json=options)
            response.raise_for_status()
            data = response.json()
            if callback:
                callback(data)
            return data

        except requests.exceptions.RequestException as e:
            if fallback:
                fallback(str(e))


class TextToMusic(BaseLLM):
    """
    Text-to-music language model.
    """
    def run(self, options, callback=None, fallback=None):
        try:
            response = requests.post(self.endpoint, headers=self.headers, json=options)
            response.raise_for_status()
            music_data = response.content  # Handle music as binary content
            if callback:
                callback(music_data)
            return music_data

        except requests.exceptions.RequestException as e:
            if fallback:
                fallback(str(e))


class LLMModelList(BaseLLM):
    """
    List of available language models.
    """
    def run(self, options=None, callback=None, fallback=None):
        try:
            response = requests.get(self.endpoint, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            if callback:
                callback(data)
            return data

        except requests.exceptions.RequestException as e:
            if fallback:
                fallback(str(e))


def LLMFactory(llm_provider, type_, token):
    """
    Factory function to create language model instances based on the provider and type.
    """
    provider = llm_provider.lower()
    endpoint = ""

    endpoints = {
        "text-to-text": {
            "openai": "https://api.openai.com/v1/chat/completions",
            "groq": "https://api.groq.com/openai/v1/chat/completions",
            "cerebras": "https://api.cerebras.ai/v1/chat/completions",
            "mistral": "https://api.mistral.ai/v1/chat/completions",
            "infodev": "https://zara.infodev.ovh/v1/chat/completions",
        },
        "text-to-speech": {
            "openai": "https://api.openai.com/v1/audio/speech",
            "groq": "https://api.groq.io/v1/synthesize",
            "cerebras": "https://api.cerebras.io/v1/synthesize",
            "mistral": "https://api.mistral.io/v1/synthesize",
            "infodev": "https://zara.infodev.ovh/v1/audio/speech",
        },
        "speech-to-text": {
            "openai": "https://api.openai.com/v1/audio/transcriptions",
            "groq": "https://api.groq.io/v1/audio/transcriptions",
            "cerebras": "https://api.cerebras.io/v1/audio/transcriptions",
            "mistral": "https://api.mistral.io/v1/audio/transcriptions",
            "infodev": "https://zara.infodev.ovh/v1/audio/transcriptions",
        },
        "image-to-text": {
            "openai": "https://api.openai.com/v1/recognize",
            "groq": "https://api.groq.io/v1/recognize",
            "cerebras": "https://api.cerebras.io/v1/recognize",
            "mistral": "https://api.mistral.io/v1/recognize",
            "infodev": "https://zara.infodev.ovh/v1/recognize",
        },
        "text-to-image": {
            "openai": "https://api.openai.com/v1/images/generations",
            "groq": "https://api.groq.io/v1/images/generations",
            "cerebras": "https://api.cerebras.io/v1/images/generations",
            "mistral": "https://api.mistral.io/v1/images/generations",
            "infodev": "https://zara.infodev.ovh/v1/images/generations",
        },
        "model-list": {
            "openai": "https://api.openai.com/v1/models",
            "groq": "https://api.groq.com/openai/v1/models",
            "cerebras": "https://api.cerebras.ai/v1/models",
            "mistral": "https://api.mistral.ai/v1/models",
            "infodev": "https://zara.infodev.ovh/v1/models",
        },
        "text-to-music": {
            "infodev": "https://zara.infodev.ovh/v1/music/generations",
        },
    }

    if type_ in endpoints and provider in endpoints[type_]:
        endpoint = endpoints[type_][provider]
    else:
        raise ValueError("Unsupported type or provider.")

    classes = {
        "text-to-text": TextToText,
        "text-to-speech": TextToSpeech,
        "speech-to-text": SpeechToText,
        "image-to-text": ImageToText,
        "text-to-image": TextToImage,
        "model-list": LLMModelList,
        "text-to-music": TextToMusic,
    }

    if type_ in classes:
        return classes[type_](endpoint, token)
    else:
        raise ValueError("Unsupported type.")
