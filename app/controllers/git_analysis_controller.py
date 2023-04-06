import asyncio
from datetime import datetime

import git
from flask import jsonify

from app.db.session import get_db_session
from app.models.analise_git_model import GitAnalysisResult
from app.utils.hidefile import hide_file


async def analisar_repositorio(repo_url, repo_dir):
    """Analisa o repositório e retorna as médias de commits por dia por desenvolvedor."""

    # Esconde o diretório do repositório local
    folder = hide_file(repo_dir)

    # Clona o repositório
    repo = await asyncio.to_thread(git.Repo.clone_from, repo_url, folder)

    # Inicializa dicionário para armazenar os commits por desenvolvedor
    commits_por_desenvolvedor = {}

    # Inicializa o dicionário para armazenar o número de dias
    dias_por_desenvolvedor = {}

    # Itera pelo histórico de commit
    for commit in repo.iter_commits():
        # Obtem o nome do autor
        autor = commit.author.name

        # Se o autor não estiver no dicionário inicia com 0
        if autor not in commits_por_desenvolvedor:
            commits_por_desenvolvedor[autor] = 0
            dias_por_desenvolvedor[autor] = set()

        # Adiciona mais um ao autor
        commits_por_desenvolvedor[autor] += 1

        # Adiciona a data de commit ao set de datas do autor
        data_commit = commit.committed_datetime.date()
        dias_por_desenvolvedor[autor].add(data_commit)

    # Calcula a média de commits por dia por desenvolvedor
    medias_por_desenvolvedor = {}

    for autor, commits in commits_por_desenvolvedor.items():
        dias = len(dias_por_desenvolvedor[autor])
        media_commits_por_dia = commits / dias if dias > 0 else 0
        medias_por_desenvolvedor[autor] = media_commits_por_dia

    return medias_por_desenvolvedor


async def git_analysis_controller(usuario, repositorio):
    """Rota para a página de análise de repositórios do GitHub."""

    # Define o diretório local
    repo_dir = 'directory\diretorio_local_repositorio'

    response = {'results': []}

    # Verifica se os parâmetros da solicitação são válidos
    if not usuario or not repositorio:
        return 'Solicitação inválida', 404, {'Content-Type': 'application/json; charset=utf-8'}

    repo_url = f'https://github.com/{usuario}/{repositorio}.git'

    # Analisa o repositório e obtém os dados relevantes
    try:
        medias_por_desenvolvedor = await analisar_repositorio(repo_url, repo_dir)
    except PermissionError as e:
        return jsonify({'error': f"Erro ao remover diretório: {e}"}), 500, {
            'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return jsonify({'error': f"Erro ao remover diretório: {e}"}), 500, {
            'Content-Type': 'application/json; charset=utf-8'}

    # Cria a resposta a ser retornada

    for autor, media_commits_por_dia in medias_por_desenvolvedor.items():
        response['results'].append({
            'author': autor,
            'commits': medias_por_desenvolvedor[autor],
            'average_commits': media_commits_por_dia,
            'repository_url': repo_url,
            'repository_name': repositorio,
            'analyze_date': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        })

        session = get_db_session()

        # Cria um novo GitAnalysisResult para persistir no banco
        result = GitAnalysisResult()
        result.author = autor
        result.analyze_date = datetime.now()
        result.average_commits = medias_por_desenvolvedor[autor]
        result.commits = media_commits_por_dia
        result.repository_url = repo_url
        result.repository_name = repositorio

        # Adiciona o objeto GitAnalysisResult na transação e fazer o commit no banco
        session.add(result)
        session.commit()
        session.close()

    return jsonify(response), 200, {'Content-Type': 'application/json; charset=utf-8'}
