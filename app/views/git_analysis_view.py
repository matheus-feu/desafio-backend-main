from flask import Blueprint
from flask import request

from app.controllers.git_analysis_controller import git_analysis_controller

bp_git_analyzer = Blueprint('git_analyzer', __name__)


@bp_git_analyzer.route('/analisador-git', methods=['GET'])
async def git_analysis():
    """Rota para a página de análise de repositórios do GitHub."""

    # Parâmetros da requisição
    usuario = request.args.get('usuario')
    repositorio = request.args.get('repositorio')

    return await git_analysis_controller(usuario, repositorio)
