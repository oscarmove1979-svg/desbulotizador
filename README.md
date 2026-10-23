# desBULOtizador

Prototipo cloud de investigación y vídeos explicativos sobre afirmaciones públicas, con presupuesto objetivo **0 €** y metodología imparcial.

## Estado real

- **Implementado:** descubrimiento RSS (por defecto BOE), cola deduplicada, expedientes preliminares, comprobaciones de estructura de evidencias, informe sin veredicto, controles editoriales, métricas y vídeo vertical diagnóstico mediante FFmpeg.
- **Experimental:** síntesis neural en español con `edge-tts`, mezcla de audio y vídeo y registro explícito del éxito o fallo. Depende de un servicio externo no garantizado.
- **No implementado:** identificación fiable de bulos políticos, contraste automático de afirmaciones con fuentes primarias, valoración editorial fiable, guiones de desmentidos reales y publicación en YouTube.
- **Sin confirmar:** ejecución satisfactoria completa en GitHub Actions. Tener código y pruebas en el repositorio no significa que el workflow haya pasado.

## Límites editoriales

Una noticia, un dato numérico, un RSS, una cita o una URL **no demuestran que exista un bulo**. Los candidatos y expedientes permanecen sin verificar. La publicación pública está bloqueada por diseño.

## Ejecución en GitHub

El workflow `.github/workflows/pipeline.yml` se ha configurado para push, ejecución manual y ejecución diaria. Cuando se ejecuta, guarda artefactos de diagnóstico: JSON de descubrimiento, cola, expedientes, voz, métricas, informes y MP4. La prueba de voz puede fallar sin habilitar publicación.

Consulta la pestaña **Actions** del repositorio para conocer el estado real de cada ejecución y descargar sus artefactos. Los archivos de salida se conservan temporalmente.

## Principios

Mismo método para todos los partidos; fuentes primarias y contexto; rectificaciones; abstención ante evidencia insuficiente; coste objetivo cero; ninguna publicación automática sin validación.

## Desarrollo

`python -m unittest discover -s tests -v` ejecuta las pruebas. Algunas requieren FFmpeg/FFprobe. El acceso a red es necesario para RSS y para el sintetizador experimental.
