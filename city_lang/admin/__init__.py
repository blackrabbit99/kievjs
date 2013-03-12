from flask import Blueprint
from city_lang.core.decorators import lazy_rule


bp = Blueprint('admin', __name__, url_prefix='/admin')

import views


lazy_rule(bp, 'speakers', {'id': None}, 'city_lang.admin.views.SpeakerView')
lazy_rule(bp, 'sponsors', {'id': None}, 'city_lang.admin.views.SponsorView')
lazy_rule(bp, 'pages', {'id': None}, 'city_lang.admin.views.PageView')
lazy_rule(bp, 'letters', {'id': None}, 'city_lang.admin.views.LetterView')
