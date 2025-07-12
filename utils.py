import os
import json
import re
from configparser import ConfigParser

HOME = os.path.expanduser("~")
PLUGIN_DIR = os.path.join(HOME, ".local", "share", "nvim", "site", "pack", "plugins")
CONFIG_DIR = os.path.join(HOME, ".config", "nvim", "plugin_tool")
BACKUP_DIR = os.path.join(CONFIG_DIR, "backups")
LUA_PLUGINS_DIR = os.path.join(HOME, ".config", "nvim", "lua", "plugins")
LUA_PLUGINS_CORE_DIR = os.path.join(HOME, ".config", "nvim", "lua", "core")
INIT_LUA_FILE = os.path.join(HOME, ".config", "nvim", "init.lua")
JSON_FILE = os.path.join(HOME,".config", "nvim", "plugins.json")


def log_action(action, plugin_name=None, status="in-progress"):
    status_icons = {
        "in-progress": "🔄",
        "success": "✅",
        "skipped": "⏭️",
        "fail": "❌",
        "info": "ℹ️"
    }

    prefix = status_icons.get(status, "")
    if plugin_name:
        print(f"{prefix} [{plugin_name}] {action}")
    else:
        print(f"{prefix} {action}")


def load_plugins():
    try:
        if not os.path.exists(JSON_FILE):
            print("No plugins found in plugins.json")
            return []
        with open(JSON_FILE, "r") as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"❌ Failed to load plugins: {e}")
        return []


def save_plugins(plugins):
    try:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(JSON_FILE, "w") as f:
            json.dump(plugins, f, indent=2)
        return True
    except (IOError, OSError) as e:
        print(f"❌ Failed to save plugins.json: {e}")
        return False


def check_if_repo_dir_exists(directory, name):
    if os.path.exists(directory):
        print(f"{name} already exists at {directory}")
        return True
    return False


def get_git_repo_url(plugin_path):
    config_path = os.path.join(plugin_path, ".git", "config")
    if not os.path.isfile(config_path):
        return None

    parser = ConfigParser()
    try:
        parser.read(config_path)
        url = parser.get('remote "origin"', "url")

        if url.startswith("git@github.com:"):
            url = url.replace("git@github.com:", "https://github.com/")
        if url.endswith(".git"):
            url = url[:-4]
        if "github.com/" in url:
            return url.split("github.com/")[1]
        return None
    except Exception as e:
        print(f"❌ Failed to read git config for {plugin_path}: {e}")
        return None


def get_existing_plugins_by_type():
    found = []
    for plugin_type in ["start", "opt"]:
        dir_path = os.path.join(PLUGIN_DIR, plugin_type)
        if not os.path.exists(dir_path):
            continue
        for name in os.listdir(dir_path):
            full_path = os.path.join(dir_path, name)
            if os.path.isdir(full_path):
                found.append({
                    "name": name,
                    "type": plugin_type,
                    "path": full_path
                })
    return found


def get_orphaned_plugins(plugins=None):
    if plugins is None:
        plugins = load_plugins()
    existing_names = {p["name"] for p in get_existing_plugins_by_type()}
    orphaned_plugins = [
        plugin for plugin in plugins
        if plugin["name"] not in existing_names
    ]

    return orphaned_plugins, existing_names


def normalize_plugin_name(name):
    if name.endswith(".nvim"):
        return name.replace(".nvim", "")
    return name


def filter_plugins_by_name(plugins, names):
    normalized_targets = [normalize_plugin_name(n) for n in names]
    result = []
    for plugin in plugins:
        normalized_plugin_name = normalize_plugin_name(plugin["name"])
        if normalized_plugin_name in normalized_targets:
            result.append(plugin)
    return result


def extract_require_names_from_init():
    if not os.path.isfile(INIT_LUA_FILE):
        return []

    pattern = re.compile(r'require\(["\']plugins\.([^"\']+)["\']\)')
    names = []

    with open(INIT_LUA_FILE, "r") as f:
        for line in f:
            match = pattern.search(line)
            if match:
                names.append(match.group(1))
    return names


def extract_lua_plugin_names(dir_path):
    if not os.path.isdir(dir_path):
        return []

    files = os.listdir(dir_path)
    lua_files = [os.path.splitext(f)[0] for f in files if f.endswith(".lua")]
    return lua_files


def extract_all_lua_plugin_names():
    plugins = extract_lua_plugin_names(LUA_PLUGINS_DIR)
    core = extract_lua_plugin_names(LUA_PLUGINS_CORE_DIR)
    return list(set(plugins + core))


def resolve_plugin_sources(name):
    normalized = normalize_plugin_name(name)

    plugins = load_plugins()
    json_entry = next((p for p in plugins if normalize_plugin_name(p["name"]) == normalized), None)

    repo_info = None
    for plugin_type in ["start", "opt"]:
        path = os.path.join(PLUGIN_DIR, plugin_type, name)
        if os.path.isdir(path):
            repo_info = {'type': plugin_type, "path":path}
            break

    config_path = os.path.join(LUA_PLUGINS_DIR, f"{normalized}.lua")
    config_exists = os.path.isfile(config_path)

    requires = extract_require_names_from_init()
    require_exists = normalized in requires

    return {
        "name": name,
        "json": json_entry,
        "repo": repo_info,
        "config_exists": config_exists,
        "require_exists": require_exists
    }


def plugin_exists_in_json(plugins, name):
    return any(p["name"] == name for p in plugins)


def prompt_yes_no(question):
    while True:
        reply = input(f"{question} [y/n]: ").strip().lower()
        if reply in ("y", "yes"):
            return True
        elif reply in ("n", "no"):
            return False
        else:
            print("Please enter 'y' or 'n'.")
