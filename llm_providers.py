"""
llm_providers.py - Provider LLM Unificado
==========================================

Rota primária: z-ai/glm-5 via OpenRouter (OPENROUTER_API_KEY)
Fallback:      Claude Sonnet 4.5 via Anthropic (ANTHROPIC_API_KEY)

Inclui AnthropicCompatWrapper — substituto drop-in para anthropic.Anthropic()
que chama OpenRouter internamente, permitindo redirecionar todas as chamadas
internas (extração de fatos, flush, consolidação) sem alterar os módulos
consumidores.
"""

import os
import logging
from typing import Optional
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

# ============================================================
# CONFIGURAÇÃO
# ============================================================

DEFAULT_MODEL = os.getenv("INTERNAL_MODEL", "z-ai/glm-5")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
VENICE_BASE_URL = os.getenv("VENICE_BASE_URL", "https://api.venice.ai/api/v1")
VENICE_MODEL = os.getenv("VENICE_MODEL", "venice-uncensored")


# ============================================================
# ANTHROPIC COMPAT WRAPPER
# Imita a interface anthropic.Anthropic().messages.create()
# mas chama OpenRouter internamente.
# Usado para redirecionar fact_extractor, consolidação, flush,
# identity extractor etc. sem alterar nenhum desses módulos.
# ============================================================

class _Content:
    def __init__(self, text: str):
        self.text = text


class _AnthropicFakeResponse:
    def __init__(self, text: str):
        self.content = [_Content(text)]


class _AnthropicFakeMessages:
    def __init__(self, openrouter_client, model: str):
        self._client = openrouter_client
        self._model = model

    def create(self, model=None, max_tokens=2000, temperature=0.7,
               messages=None, system=None, **kwargs):
        msgs = list(messages or [])
        if system:
            msgs = [{"role": "system", "content": system}] + msgs
        resp = self._client.chat.completions.create(
            model=self._model,          # sempre z-ai/glm-5 (ignora `model` passado)
            max_tokens=max_tokens,
            temperature=temperature,
            messages=msgs,
        )
        return _AnthropicFakeResponse(resp.choices[0].message.content)


class AnthropicCompatWrapper:
    """
    Substituto drop-in para anthropic.Anthropic() que usa OpenRouter internamente.

    Suporta:
        client.messages.create(model=..., max_tokens=..., temperature=...,
                                messages=[...], system=...) → response.content[0].text

    O parâmetro `model` é ignorado — sempre usa o modelo configurado em INTERNAL_MODEL.
    """

    def __init__(self, openrouter_client, model: str = DEFAULT_MODEL):
        self.messages = _AnthropicFakeMessages(openrouter_client, model)
        logger.info(f"✅ AnthropicCompatWrapper inicializado (modelo: {model} via OpenRouter)")


# ============================================================
# ABSTRACT BASE CLASS (mantida para compatibilidade)
# ============================================================

class LLMProvider(ABC):
    """Interface abstrata para provedores de LLM"""

    @abstractmethod
    def get_response(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Gera resposta do LLM"""
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """Retorna nome do modelo sendo usado"""
        pass


# ============================================================
# OPENROUTER PROVIDER (PRIMÁRIO)
# ============================================================

class OpenRouterProvider(LLMProvider):
    """Provedor via OpenRouter — primário para todos os LLM calls."""

    def __init__(self, model: str = DEFAULT_MODEL):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("❌ OPENROUTER_API_KEY não encontrado no .env")
        self.model = model
        logger.info(f"✅ OpenRouterProvider inicializado (modelo: {self.model})")

    def get_response(self, prompt: str, temperature: float = 0.7,
                     max_tokens: int = 2000) -> str:
        from openai import OpenAI
        client = OpenAI(base_url=OPENROUTER_BASE_URL, api_key=self.api_key)
        try:
            resp = client.chat.completions.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.choices[0].message.content
        except Exception as e:
            logger.error(f"❌ Erro ao chamar OpenRouter: {e}")
            raise Exception(f"Erro ao chamar OpenRouter: {e}")

    def get_model_name(self) -> str:
        return f"OpenRouter ({self.model})"


# ============================================================
# CLAUDE PROVIDER (FALLBACK)
# ============================================================

class ClaudeProvider(LLMProvider):
    """Provedor Claude via Anthropic — fallback quando OpenRouter não disponível."""

    def __init__(self, model: str = "claude-sonnet-4-5-20250929"):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("❌ ANTHROPIC_API_KEY não encontrado no .env")
        self.model = model
        logger.info(f"✅ ClaudeProvider inicializado (modelo: {self.model})")

    def get_response(self, prompt: str, temperature: float = 0.7,
                     max_tokens: int = 2000) -> str:
        try:
            import anthropic
        except ImportError:
            raise ImportError("❌ Biblioteca 'anthropic' não instalada")
        try:
            client = anthropic.Anthropic(api_key=self.api_key)
            message = client.messages.create(
                model=self.model, max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            logger.error(f"❌ Erro ao chamar Claude API: {e}")
            raise Exception(f"Erro ao chamar Claude API: {e}")

    def get_model_name(self) -> str:
        return f"Claude ({self.model})"


# ============================================================
# ============================================================
# VENICE PROVIDER (privado, sem censura)
# ============================================================
class VeniceProvider(LLMProvider):
    """Provedor via Venice.ai — privado, uncensored, OpenAI-compatible."""

    def __init__(self, model: str = VENICE_MODEL):
        self.api_key = os.getenv("VENICE_API_KEY")
        if not self.api_key:
            raise ValueError("❌ VENICE_API_KEY não encontrado no .env")
        self.model = model
        logger.info(f"✅ VeniceProvider inicializado (modelo: {self.model})")

    def get_response(self, prompt: str, temperature: float = 0.7,
                     max_tokens: int = 2000) -> str:
        from openai import OpenAI
        client = OpenAI(base_url=VENICE_BASE_URL, api_key=self.api_key)
        try:
            resp = client.chat.completions.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.choices[0].message.content
        except Exception as e:
            logger.error(f"❌ Erro ao chamar Venice: {e}")
            raise Exception(f"Erro ao chamar Venice: {e}")

    def get_model_name(self) -> str:
        return f"Venice ({self.model})"


# FACTORY — Venice ou OpenRouter primário, Claude fallback
# ============================================================

def create_llm_provider(provider_name: Optional[str] = None) -> LLMProvider:
    if provider_name == "venice" and os.getenv("VENICE_API_KEY"):
        logger.info(f"🔧 Criando LLM Provider: Venice ({VENICE_MODEL})")
        return VeniceProvider()
    if os.getenv("LLM_PROVIDER", "").strip().lower() == "venice" and os.getenv("VENICE_API_KEY"):
        logger.info(f"🔧 Criando LLM Provider: Venice ({VENICE_MODEL})")
        return VeniceProvider()
    if os.getenv("OPENROUTER_API_KEY"):
        logger.info(f"🔧 Criando LLM Provider: OpenRouter ({DEFAULT_MODEL})")
        return OpenRouterProvider()
    logger.info("🔧 Criando LLM Provider: Claude (fallback)")
    return ClaudeProvider()


# ============================================================
# HELPER FUNCTION (compatibilidade)
# ============================================================

# Singleton global do provider (inicializado na primeira chamada)
_provider_instance: Optional[LLMProvider] = None

def get_llm_response(
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 2000
) -> str:
    """
    Função auxiliar para obter resposta do LLM.

    Usa Claude Sonnet 4.5 como único provider.
    O provider é inicializado apenas uma vez (singleton).

    Args:
        prompt: Prompt para o LLM
        temperature: Temperatura (0.0 = determinístico, 1.0 = criativo)
        max_tokens: Máximo de tokens na resposta

    Returns:
        Resposta do LLM como string

    Example:
        response = get_llm_response("Explique arquétipos junguianos", temperature=0.8)
    """

    global _provider_instance

    if _provider_instance is None:
        _provider_instance = create_llm_provider()
        logger.info(f"✅ LLM Provider ativado: {_provider_instance.get_model_name()}")

    return _provider_instance.get_response(prompt, temperature, max_tokens)


def get_current_model_name() -> str:
    """Retorna nome do modelo LLM atualmente ativo"""

    global _provider_instance

    if _provider_instance is None:
        _provider_instance = create_llm_provider()

    return _provider_instance.get_model_name()


def reset_provider():
    """Reseta o singleton do provider (útil para testes)"""
    global _provider_instance
    _provider_instance = None
    logger.info("🔄 LLM Provider resetado")


# ============================================================
# TESTES
# ============================================================

if __name__ == "__main__":
    """Testes básicos"""

    logging.basicConfig(level=logging.INFO)

    print("="*60)
    print("TESTE: LLM Provider (Claude Sonnet 4.5)")
    print("="*60)

    print(f"\nModelo configurado: {DEFAULT_MODEL}")

    try:
        response = get_llm_response(
            "Responda em uma palavra: qual a cor do céu?",
            max_tokens=10
        )
        print(f"✅ Claude respondeu: {response}")
        print(f"   Modelo: {get_current_model_name()}")
    except Exception as e:
        print(f"❌ Erro: {e}")

    print("\n" + "="*60)
    print("✅ Teste concluído")
    print("="*60)
