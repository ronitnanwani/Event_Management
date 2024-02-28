from . import *
app_views = Blueprint('app_views', __name__)

@app_views.route('/')
def index():
    return render_template('test.html', name='orld')
