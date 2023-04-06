from flask import jsonify

from app.db.session import get_db_session
from app.models.analise_git_model import GitAnalysisResult


async def controller_search_commit(autor1, autor2, autor3):
    """Controlador do endpoint, responsável por buscar análises de commits já realizadas
    anteriormente."""

    autores = [autor1, autor2, autor3]

    session = get_db_session()

    resultados = {'results': []}

    for autor in autores:
        for registro in session.query(GitAnalysisResult).filter(GitAnalysisResult.author.ilike(f'%{autor}%')).all():
            resultados['results'].append(f'{registro.author} possui uma média de {registro.average_commits:.2f} commits por dia.')

    resultados_nao_duplicados = list(set(resultados['results']))  # Removendo resultados repetidos do banco de dados
    return jsonify({'results': resultados_nao_duplicados}), 200, {'Content-Type': 'application/json;charset=utf-8'}
