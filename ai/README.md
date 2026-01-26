Integración rápida:
1. Importa getPolicyForJob(meta) en el orquestador que crea la sesión/chat.
2. Al recibir la solicitud del usuario, construir JobMeta y pedir policy.
3. Si policy.autoSummarize es true, aplicar quickSummarize() al contexto antes de enviar al motor.
4. Respetar policy.maxInteractions para esa sesión; si se alcanza, sugerir dividir en subtareas cuando suggestSplit=true.
5. Registrar métricas definidas en adaptive_limits.json para ajustar umbrales.
