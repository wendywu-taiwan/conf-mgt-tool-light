

def get_single_model(class_model, **kwargs):
    try:
        return class_model.objects.filter(**kwargs).first()
    except class_model.DoesNotExist:
        return None


def get_models(class_model, **kwargs):
    try:
        return class_model.objects.filter(**kwargs)
    except class_model.DoesNotExist:
        return None


def get_value(class_model, key):
    try:
        return class_model.objects.only(key)
    except class_model.DoesNotExist:
        return None
