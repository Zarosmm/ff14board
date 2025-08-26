import requests
import uuid
import random
import copy

BASE_URL = 'http://127.0.0.1:8080/api'
ADMIN_URL = 'http://127.0.0.1:8080/admin'

AUTH_HEADER = {
    'Authorization': 'Bearer 123'  # 替换为实际 token
}

# ---------- 通用函数 ----------
def get(endpoint):
    url = f"{ADMIN_URL}/{endpoint}?is_page=False"
    r = requests.get(url)
    if r.status_code == 200:
        print(r.json())
        return r.json()['data']
    print(f"Get {url} failed: {r.status_code} - {r.text}")
    return None

def retrieve(endpoint, instance_id):
    url = f"{ADMIN_URL}/{endpoint}/{instance_id}"
    r = requests.get(url)
    if r.status_code == 200:
        print(r.json())
        return r.json()['data']
    print(f"Get {url} failed: {r.status_code} - {r.text}")
    return None

def postBase(url, payload):
    global AUTH_HEADER
    if url == "http://localhost:8000/register":
        AUTH_HEADER = {}
    r = requests.post(url, json=payload, headers=AUTH_HEADER)
    if r.status_code in (200, 201):
        print(r.json())
        return r.json()['data']
    print(f"POST {url} failed: {r.status_code} - {r.text}")
    return None

def post(endpoint, payload):
    url = f"{BASE_URL}/{endpoint}/"
    return postBase(url, payload)

def putBase(baseurl, instance_id, payload):
    url = f"{baseurl}/{instance_id}/"
    r = requests.put(url, json=payload, headers=AUTH_HEADER)
    if r.status_code == 200:
        print(r.json()['data'])
        return r.json()['data']
    print(f"PUT {baseurl}/{instance_id} failed: {r.status_code} - {r.text}")
    return None

def put(endpoint, instance_id, payload):
    url = f"{ADMIN_URL}/{endpoint}"
    return putBase(url, instance_id, payload)

def deleteBase(baseurl, instance_id):
    url = f"{baseurl}/{instance_id}/"
    r = requests.delete(url, headers=AUTH_HEADER)
    if r.status_code in (200, 204):
        print(r.json())
        return True
    print(f"DELETE {baseurl}/{instance_id} failed: {r.status_code} - {r.text}")
    return False

def delete(endpoint, instance_id):
    url = f"{ADMIN_URL}/{endpoint}"
    return deleteBase(url, instance_id)

# ---------- 创建实例 ----------
created_servers = []
created_users = []
created_characters = []
created_teams = []
try:
    # 1. 创建无父 server
    root_server = post("server", {"name": "Root Server"})
    created_servers.append(root_server)

    # 2. 创建两个子 server
    server_a = post("server", {"name": "Server A", "parent": root_server['id']})
    server_b = post("server", {"name": "Server B", "parent": root_server['id']})
    created_servers.extend([server_a, server_b])

    # 3. 创建 8 个用户，每个 1~2 个角色
    for i in range(8):
        user = postBase("http://localhost:8080/register", {
            "email": f"user{i}@example.com",
            "username": f"username{i}",
            "password": "password123",
        })
        if not user:
            break
        retrieve('user', user['id'])
        created_users.append(user)
        access_token = postBase("http://localhost:8080/login", {"username": f"username{i}", "password": "password123"})["access_token"]
        user["token"] = access_token
        print(1111111111111111111)
        # 创建 1~2 个角色
        num_characters = random.randint(1,2)
        print(num_characters)
        user_characters = []
        for j in range(num_characters):
            server_choice = random.choice([server_a, server_b])
            character = post("character", {
                "user": user['id'],
                "server": server_choice['id'],
                "name": f"Character {i}-{j}",
                "jobs": random.sample(["Warrior", "Mage", "Archer"], 1)
            })
            user_characters.append(character)
            created_characters.append(character)
        user['character'] = user_characters

    # ---------- 修改部分实例 ----------
    # 修改一个 server 的名称
    updated_server_a = put("server", server_a['id'], {"name": "Server A Updated"})
    #created_servers[1] = updated_server_a

    # 修改一个 user 的头像
    updated_user0 = put("user", created_users[0]['id'], {"avatar_url": "http://example.com/new_avatar.png"})
    #created_users[0] = updated_user0

    # 修改一个角色的 jobs
    character_to_update = created_characters[0]
    updated_character = put("character", character_to_update['id'], {"jobs": ["Healer", "Mage"]})
    #created_characters[0] = updated_character

    # ---------- 创建团队 ----------
    leader_user = created_users[0]
    leader_character = leader_user['character'][0]

    # 其他用户选一个角色作为 member
    members = []
    # get('character')
    for u in created_users[1:]:
        print(u['character'])
    for u in created_users[1:]:
        members.append(u['character'][0])

    team_payload = {
        "name": "Test Team",
        "leader": leader_character['id'],
        "members": [m['id'] for m in members],
        "time_slots": ["Monday 10AM", "Wednesday 2PM"]
    }
    team = post("team", team_payload)
    created_teams.append(team)

    # 修改团队名称
    updated_team = putBase("http://127.0.0.1:8080/api/team", team['id'], {"name": "Test Team Updated"})
    #created_teams[0] = updated_team

    # ---------- 打印当前创建的实例 ID ----------
    print("Created Servers:", [s['id'] for s in created_servers])
    print("Created Users:", [u['id'] for u in created_users])
    print("Created Characters:", [c['id'] for c in created_characters])
    print("Created Teams:", [t['id'] for t in created_teams])
except Exception as e:
    print(e)
# ---------- 删除实例（顺序：Team -> Character -> User -> Server） ----------
# 删除团队
try:
    for t in created_teams:
        deleteBase("http://127.0.0.1:8080/api/team", t['id'])
except Exception as e:
    print(f"Delete Team failed with {e}")

try:
    # 删除角色
    for c in created_characters:
        delete("character", c['id'])
except Exception as e:
    print(f"Delete Character failed with {e}")

try:
    # 删除用户
    for u in created_users:
        delete("user", u['id'])
except Exception as e:
    print(f"Delete User failed with {e}")


try:
    # 删除服务器（先子 server 再 root server）
    for s in created_servers[1:]:
        delete("server", s['id'])
    delete("server", created_servers[0]['id'])
except Exception as e:
    print(f"Delete Server failed with {e}")

print("All instances deleted.")
