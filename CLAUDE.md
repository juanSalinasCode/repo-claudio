# Instrucciones para Claude

- Responde en español.
- **Al final de CADA respuesta**, llama a la herramienta `get_session` (servidor
  `claude-code-remote`, sin `session_id`) y añade un bloque de uso con lo que devuelva
  `external_metadata`:

  ```
  📊 Uso
  • Límite (rate_limit_info.rateLimitType): estado (status), reinicia a las HH:MM (resetsAt, hora local del usuario si se conoce; si no, UTC) — en X h Y min
  • Usando extra/overage: sí/no (isUsingOverage)
  • Contexto: used_tokens / max_tokens (porcentaje)
  • Sesión: ~$cost_usd equivalentes en API · tokens salida output_tokens
  ```

  Si un dato no aparece, omítelo; nunca inventes un porcentaje del límite que la
  herramienta no da. Si `get_session` no está disponible (por ejemplo al trabajar en local),
  indica que el uso se ve con `/usage` o en la barra de estado.
