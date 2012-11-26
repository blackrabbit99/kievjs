from werkzeug import import_string, cached_property


class ClassProperty(property):
    def __init__(self, method, *args, **kwargs):
        method = classmethod(method)
        return super(ClassProperty, self).__init__(method, *args, **kwargs)

    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


classproperty = ClassProperty


class LazyResource(object):

    def __init__(self, import_name, endpoint):
        self.__module__, self.__name__ = import_name.rsplit('.', 1)
        self.import_name = import_name
        self.endpoint = endpoint

    @cached_property
    def view(self):
        view_class = import_string(self.import_name)
        view_class.endpoint = self.endpoint
        return view_class.as_view(self.endpoint)

    def __call__(self, *args, **kwargs):
        return self.view(*args, **kwargs)


def lazy_rule(bp, endpoint, pk_def, import_name):
    resource = LazyResource(import_name, endpoint)
    collection_url = "/{}/".format(endpoint)
    # collection endpoint

    pk = pk_def.keys()[0]
    pk_type = pk_def[pk] and pk_def[pk].__name__ or None

    if pk_type is None:
        item_url = "%s<%s>" % (collection_url, pk)
    else:
        item_url = "%s<%s:%s>" % (collection_url, pk_type, pk)

    bp.add_url_rule(collection_url, view_func=resource,
                    methods=['GET', 'POST'])
    bp.add_url_rule(item_url, view_func=resource,
                    methods=['GET', 'PUT', 'DELETE'])

