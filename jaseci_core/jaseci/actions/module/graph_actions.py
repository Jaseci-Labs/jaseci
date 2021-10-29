def max(param_list, meta):
    ret = None
    if (not len(param_list)):
        return None
    items = param_list[0].obj_list()
    if (not len(items)):
        return None
    max_val = items[0].anchor_value()
    ret = items[0]
    for i in items:
        if(i.anchor_value() > max_val):
            ret = i
            max_val = i.anchor_value()
    return ret
