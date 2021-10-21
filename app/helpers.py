def get_size_querystring(request):
    size = 0

    if 'size' in request.args:
        if request.args['size'].isnumeric():
            size = int(request.args['size'])
        else:
            raise ValueError('Size only accept numeric values')

    return size


def get_token_querystring(request):
    if 'token' in request.args:
        return request.args['token']

    return None


def get_sort_by(attribute):
    sort_by = attribute
    attr_dic = dict(
        distance="cumulative_distance",
        time="cumulative_time",
        speed="average_speed",
    )

    if attribute in attr_dic:
        sort_by = attr_dic[attribute]

    return sort_by


def get_sorted_list(sort_by, scope, avoid_user=None, reverse=True):
    result = []
    _list = [[v[sort_by], k] for k, v in scope.items()]

    sort = sorted(_list, reverse=reverse)

    for _, v in sort:
        if avoid_user and avoid_user == v:
            continue
        result.append(scope[v])

    return result
