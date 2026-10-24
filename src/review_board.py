"""Human-readable queue of unverified research candidates."""
import json
import html
from urllib.parse import urlsplit
from pathlib import Path

def render_board(report):
    if report.get('publication_allowed') is not False:
        raise ValueError('Unsafe report')
    records = report.get('pending_claims', [])
    if not isinstance(records, list):
        raise ValueError('Invalid records')
    lines = ['# desBULOtizador: revision editorial', '', 'NO VERIFICADO - PUBLICACION BLOQUEADA', '']
    if not records:
        lines.append('No hay afirmaciones pendientes en esta ejecucion.')
    for record in records:
        if not isinstance(record, dict) or record.get('status') != 'unverified' or record.get('publication_allowed') is not False:
            raise ValueError('Unsafe candidate')
        claim = record.get('claim')
        if not isinstance(claim, str) or not claim.strip():
            raise ValueError('Missing claim text')
        claim = html.escape(' '.join(claim.split()))
        source = record.get('source_url')
        if not isinstance(source, str):
            raise ValueError('Invalid source URL')
        parsed = urlsplit(source)
        if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
            raise ValueError('Source URL must use HTTPS')
        source = source.replace('\n', '').replace('\r', '')
        lines.extend(['## Afirmacion pendiente', claim, '', 'Fuente: ' + source, 'Pruebas primarias: pendientes', 'Veredicto: ninguno', ''])
    return '\n'.join(lines) + '\n'

if __name__ == '__main__':
    report = json.loads(Path('output/report.json').read_text(encoding='utf-8'))
    Path('output/review_board.md').write_text(render_board(report), encoding='utf-8')
