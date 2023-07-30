import base64
import json

def replace_server_address(vmess_link, new_server_address):
    try:
        # 解码VMess链接
        vmess_base64 = vmess_link.replace("vmess://", "")
        vmess_json = base64.urlsafe_b64decode(vmess_base64 + '=' * (4 - len(vmess_base64) % 4))
        vmess_info = json.loads(vmess_json)

        # 替换服务器地址
        vmess_info["add"] = new_server_address

        # 更新VMess链接
        updated_vmess_json = json.dumps(vmess_info, separators=(",", ":"), sort_keys=True)
        updated_vmess_base64 = base64.urlsafe_b64encode(updated_vmess_json.encode('utf-8')).decode('utf-8')
        updated_vmess_link = f"vmess://{updated_vmess_base64}"

        return updated_vmess_link

    except (base64.binascii.Error, json.JSONDecodeError):
        return None

if __name__ == "__main__":
    vmess_link = input("输入原始的VMess链接: ")
    ip_addresses = []
    while True:
        ip_address = input("输入IP地址 (输入'exit'结束): ")
        if ip_address.lower() == 'exit':
            break
        ip_addresses.append(ip_address)

    updated_vmess_links = []

    for ip_address in ip_addresses:
        updated_vmess_link = replace_server_address(vmess_link, ip_address)
        if updated_vmess_link:
            updated_vmess_links.append(updated_vmess_link)

    if updated_vmess_links:
        with open("updated_vmess_links.txt", "w") as f:
            f.write("\n".join(updated_vmess_links))
        print("已将更新后的VMess链接导出到 updated_vmess_links.txt 文件中。")
    else:
        print("无效的VMess链接或解析失败。请确保输入的是有效的VMess链接和IP地址。")
