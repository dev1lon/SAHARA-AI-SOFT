async def format_proxy(proxy: str) -> dict:
    username_password, server_port = proxy.replace('http://', '').split('@')
    username, password = username_password.split(':')
    server, port = server_port.split(':')
    proxy = {
        "server": f"http://{server}:{port}",
        "username": username,
        "password": password,
    }
    return proxy


def read_file(filepath):
    with open(filepath) as file:
        return [line.strip() for line in file.readlines()]


def parse_params(
        params: str,
        has_function_signature: bool = True
) -> None:

    if has_function_signature:
        function_signature = params[:10]
        print('Function signature:', function_signature)
        params = params[10:]
    else:
        params = params[2:]

    count = 0
    while params:
        memory_address = hex(count * 32)[2:].zfill(3)
        print(f'{memory_address}: {params[:64]}')
        count += 1
        params = params[64:]
    print()
