"""
Módulo del servicio de integración con Google Gemini AI.

Implementa la comunicación con la API de Google Gemini para generar
respuestas conversacionales contextuales sobre el catálogo de zapatos.
"""

import google.generativeai as genai
from typing import List
from ...config import Config
from ...domain.entities import Product, ChatContext
from ...domain.exceptions import ChatServiceError


class GeminiService:
    """
    Servicio de IA que integra Google Gemini para el chat de e-commerce.

    Configura el cliente de Gemini con la API key del entorno y genera
    respuestas contextuales que incluyen información del catálogo de
    productos y el historial de la conversación.

    Attributes:
        model: Instancia del modelo generativo de Google Gemini.
    """

    def __init__(self):
        """
        Inicializa el servicio configurando el cliente de Google Gemini.

        Lee la API key desde las variables de entorno a través de Config
        y prepara el modelo gemini-2.5-flash para generar respuestas.

        Raises:
            ChatServiceError: Si la GEMINI_API_KEY no está configurada.
        """
        if not Config.GEMINI_API_KEY:
            raise ChatServiceError(
                "GEMINI_API_KEY no está configurada. "
                "Agrega tu API key en el archivo .env"
            )
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    async def generate_response(
        self,
        user_message: str,
        products: List[Product],
        context: ChatContext,
    ) -> str:
        """
        Genera una respuesta del asistente de IA para el mensaje del usuario.

        Construye un prompt completo que incluye:
        - Instrucciones del sistema (cómo debe comportarse la IA)
        - Lista de productos disponibles en el catálogo
        - Historial de la conversación (para memoria)
        - El mensaje actual del usuario

        Args:
            user_message (str): Mensaje que el usuario acaba de enviar.
            products (List[Product]): Lista de productos del catálogo.
            context (ChatContext): Contexto con el historial reciente.

        Returns:
            str: Respuesta generada por la IA de Google Gemini.

        Raises:
            ChatServiceError: Si ocurre un error al llamar a la API de Gemini.

        Example:
            >>> response = await gemini.generate_response(
            ...     user_message="Busco zapatos Nike para correr",
            ...     products=lista_productos,
            ...     context=contexto_vacio
            ... )
            >>> print(response)
            "¡Hola! Tengo el Nike Air Zoom Pegasus disponible en talla 42..."
        """
        try:
            productos_texto = self.format_products_info(products)
            historial_texto = context.format_for_prompt()

            prompt = self._build_prompt(
                user_message=user_message,
                productos_texto=productos_texto,
                historial_texto=historial_texto,
            )

            response = self.model.generate_content(prompt)
            return response.text

        except ChatServiceError:
            raise
        except Exception as e:
            raise ChatServiceError(
                f"Error al comunicarse con Google Gemini: {str(e)}"
            )

    def format_products_info(self, products: List[Product]) -> str:
        """
        Formatea la lista de productos como texto para incluir en el prompt.

        Convierte las entidades Product a un formato de texto estructurado
        y legible para que la IA pueda entender y referenciar el catálogo.

        Args:
            products (List[Product]): Lista de entidades de productos.

        Returns:
            str: Texto con el catálogo formateado, una línea por producto.

        Example:
            >>> formato = gemini.format_products_info(productos)
            >>> print(formato)
            '- Air Zoom Pegasus 40 | Nike | Running | Talla: 42 | $120.0 | Stock: 5'
        """
        if not products:
            return "No hay productos disponibles en este momento."

        lines = []
        for p in products:
            disponibilidad = "Disponible" if p.is_available() else "Agotado"
            lines.append(
                f"- {p.name} | {p.brand} | {p.category} | "
                f"Talla: {p.size} | Color: {p.color} | "
                f"${p.price} | Stock: {p.stock} ({disponibilidad})"
            )
        return "\n".join(lines)

    def _build_prompt(
        self, user_message: str, productos_texto: str, historial_texto: str
    ) -> str:
        """
        Construye el prompt completo para enviar a Google Gemini.

        El prompt tiene varias secciones:
        1. Instrucciones del sistema (personalidad y reglas del asistente)
        2. Catálogo de productos disponibles
        3. Historial de la conversación (si existe)
        4. El mensaje actual del usuario

        Args:
            user_message (str): Mensaje actual del usuario.
            productos_texto (str): Catálogo formateado como texto.
            historial_texto (str): Historial de conversación formateado.

        Returns:
            str: Prompt completo listo para enviar a Gemini.
        """
        historial_seccion = ""
        if historial_texto:
            historial_seccion = f"""
HISTORIAL DE LA CONVERSACIÓN ANTERIOR:
{historial_texto}
"""

        return f"""Eres un asistente virtual experto en ventas de zapatos para una tienda online llamada "ZapatoShop".
Tu objetivo es ayudar a los clientes a encontrar los zapatos perfectos de manera amigable y profesional.

PRODUCTOS DISPONIBLES EN NUESTRO CATÁLOGO:
{productos_texto}

INSTRUCCIONES:
- Sé amigable, entusiasta y profesional en tus respuestas
- Usa el historial de la conversación para mantener coherencia
- Recomienda productos específicos del catálogo cuando sea apropiado
- Siempre menciona el precio, talla y disponibilidad al recomendar
- Si el producto está agotado, sugiere alternativas disponibles
- Si el cliente pregunta algo fuera del catálogo, sé honesto y redirige al tema de zapatos
- Responde siempre en español
- Mantén las respuestas concisas pero informativas (máximo 3-4 párrafos)
{historial_seccion}
MENSAJE ACTUAL DEL USUARIO:
{user_message}

RESPUESTA DEL ASISTENTE:"""
