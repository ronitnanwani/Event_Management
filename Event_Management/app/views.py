from . import *
app_views = Blueprint('app_views', __name__)

@app_views.route('/')
def index():
    return render_template('test.html', name='orld')
@app_views.route('/event')
def events():
    events=[{"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]}]
    return render_template('events.html', name='events',events=events)
