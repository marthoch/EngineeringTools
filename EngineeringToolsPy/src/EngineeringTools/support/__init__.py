def singleton(class_):
    """http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python"""
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

