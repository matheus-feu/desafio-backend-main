import pytest
from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_git_analysis_success(client):
    response = client.get('/analisador-git?usuario=gitpython-developers&repositorio=gitdb')
    assert response.status_code == 200
    assert len(response.json['results']) > 0
    assert 'author' in response.json['results'][0]
    assert 'commits' in response.json['results'][0]
    assert 'average_commits' in response.json['results'][0]
    assert 'repository_url' in response.json['results'][0]
    assert 'repository_name' in response.json['results'][0]


def test_git_analysis_invalid_request(client):
    response = client.get('/analisador-git?usuario=&repositorio=')
    assert response.status_code == 404
    assert 'Solicitação inválida' in response.data.decode('utf-8')


def test_buscar_medias_de_commit_success(client):
    response = client.get('/analisador-git/buscar?autor1=Matheus Feu')
    assert response.status_code == 200
    assert len(response.json['results']) > 0
    assert 'possui uma média de' in response.json['results'][0]


def test_buscar_medias_de_commit_no_results(client):
    response = client.get('/analisador-git/buscar?autor1=not-found')
    assert response.status_code == 200
    assert len(response.json['results']) == 0
