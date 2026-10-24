"""Human-readable queue of unverified research candidates."""
import json
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
        claim = str(record.get('claim', '')).replace('\n', ' ').replace('\r', ' ').strip()
        source = str(record.get('source_url', '')).replace('\n', '').replace('\r', '').strip()
        lines.extend(['## Afirmacion pendiente', claim, '', 'Fuente: ' + source, 'Pruebas primarias: pendientes', 'Veredicto: ninguno', ''])
    return '\n'.join(lines) + '\n'

if __name__ == '__main__':
    report = json.loads(Path('output/report.json').read_text(encoding='utf-8'))
    Path('output/review_board.md').write_text(render_board(report), encoding='utf-8')
