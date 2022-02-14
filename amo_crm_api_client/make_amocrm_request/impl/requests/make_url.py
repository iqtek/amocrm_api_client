def make_url(base_url: str, *routes):
    routes_list = list()
    base = base_url.rstrip("/")
    for route in routes:
        clear_route = route.rstrip("/").lstrip("/")
        routes_list.append(clear_route)

    result = base + "/" + "/".join(routes_list)

    return result
