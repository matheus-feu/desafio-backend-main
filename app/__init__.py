from flask import Flask

from app.views.git_analysis_view import bp_git_analyzer
from app.views.search_commit_view import bp_search_commit

app = Flask(__name__)
app.config.from_object('config')

app.register_blueprint(bp_git_analyzer)
app.register_blueprint(bp_search_commit)
