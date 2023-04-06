from flask import Blueprint, request

from app.controllers.search_commits_controller import controller_search_commit

bp_search_commit = Blueprint('bp_search_commit', __name__)


@bp_search_commit.route('/analisador-git/buscar', methods=['GET'])
async def buscar_medias_de_commit():
    """Rota para a página de busca de commits."""

    autor1 = request.args.get('autor1')
    autor2 = request.args.get('autor2')
    autor3 = request.args.get('autor3')

    return await controller_search_commit(autor1, autor2, autor3)
