from flask.ext.appbuilder import IndexView


class IndexView(IndexView):
    index_template = 'index.html'