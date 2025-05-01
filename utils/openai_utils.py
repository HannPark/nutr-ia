from semantic_kernel import Kernel
from semantic_kernel.orchestration.sk_context import SKContext

from config.openai_config import OpenAIConfig

class OpenAIUtils:
    @staticmethod
    async def ai_semantic_question(kernel: Kernel, prompt: str) -> str:
        """
        Utiliza el modelo de OpenAI para responder preguntas semánticas.
        """
        completion_function = kernel.create_semantic_function(
                prompt_template=prompt,
                max_tokens=OpenAIConfig.MAX_TOKENS,
                temperature=OpenAIConfig.TEMPERATURE
            )
        response: SKContext = await completion_function.invoke_async()
        return response.result