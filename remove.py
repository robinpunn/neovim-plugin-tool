import os
import shutil
from utils import (
    load_plugins,
    save_plugins,
    normalize_plugin_name,
    extract_require_names_from_init,
    resolve_plugin_sources,
    prompt_yes_no,
    LUA_PLUGINS_DIR,
    INIT_LUA_FILE
)
from backup import create_backup


def remove_plugins(
    names,
    force=False,
    backup=False,
    json=False,
    repo=False,
    config=False,
    require=False
):
    if not names:
        print("❌ No plugin names provided")

    plugins = load_plugins()

    if not plugins:
        print("No plugins found in plugins.json")
        return

    if not force and not backup:
        if prompt_yes_no("Would you like to create a backup before removing"):
            create_backup()
    elif backup:
        create_backup()

    specific_flags = any([json, repo, config, require])

    for name in names:
        info = resolve_plugin_sources(name)
        pretty_name = info["name"]

        if specific_flags:
            if json and not info["json"]:
                print(f"Plugin '{pretty_name}' not found in plugin.json")

            if repo and not info["repo"]:
                print(f"Plugin '{pretty_name}' repo not found")

            if config and not info["config_exists"]:
                print(f"Plugin {pretty_name}.lua not found")

            if require and not info["require_exists"]:
                print(f"Plugin {pretty_name}.lua not found")

            if json and info["json"]:
                if force or prompt_yes_no(f"Remove plugin.json entry for '{pretty_name}'?"):
                    remove_plugin_from_json(plugins, pretty_name)
            if repo and info["repo"]:
                if force or prompt_yes_no(f"Delete repo for '{pretty_name}'?"):
                    remove_plugin_repo(info["repo"])
            if config and info["config_exists"]:
                if force or prompt_yes_no(f"Remove lua config file for '{pretty_name}'?"):
                    remove_lua_config(pretty_name)
            if require and info["require_exists"]:
                if force or prompt_yes_no(f"Remove require() from init.lua for '{pretty_name}'?"):
                    remove_require_from_init(pretty_name)
        else:
            if info["json"] and (force or prompt_yes_no(f"Remove plugin.json entry for '{pretty_name}'?")):
                remove_plugin_from_json(plugins, pretty_name)
            if info["repo"] and (force or prompt_yes_no(f"Delete repo for '{pretty_name}'?")):
                remove_plugin_repo(info["repo"])
            if info["config_exists"] and (force or prompt_yes_no(f"Remove lua config file for '{pretty_name}'?")):
                remove_lua_config(pretty_name)
            if info["require_exists"] and (force or prompt_yes_no(f"Remove require() from init.lua for '{pretty_name}'?")):
                remove_require_from_init(pretty_name)


def remove_plugin_from_json(plugins, name):
    updated = [p for p in plugins if p["name"] != name]
    save_plugins(updated)
    print(f"✅ Removed {name} from plugins.json")


def remove_plugin_repo(repo_info):
    path = repo_info["path"]
    if os.path.isdir(path):
        shutil.rmtree(path)
        print(f"✅ Deleted repo: {path}")
    else:
        print(f"⚠️ Repo not found: {path}")


def remove_lua_config(name):
    normalized = normalize_plugin_name(name)
    path = os.path.join(LUA_PLUGINS_DIR, f"{normalized}.lua")
    if os.path.isfile(path):
        os.remove(path)
        print(f"✅ Deleted lua config: {path}")
        return

    print(f"⚠️ Lua config not found: {path}")


def remove_require_from_init(name):
    normalized = normalize_plugin_name(name)
    current_requires = extract_require_names_from_init()

    # require_line = f'require("plugins.{normalized}")'
    if normalized not in current_requires:
        print(f"⚠️ Require line not found in init.lua for '{name}'")

    if not os.path.isfile(INIT_LUA_FILE):
        print("⚠️ init.lua not found")
        return

    with open(INIT_LUA_FILE, "r") as f:
        lines = f.readlines()
        # print(lines)

    with open(INIT_LUA_FILE, "w") as f:
        for line in lines:
            if f'require("plugins.{normalized}")' not in line:
                f.write(line)

    print(f"✅ Removed require line from init.lua for '{name}'")


def delete_plugins_json(force=False):
    if not os.path.exists("plugins.json"):
        print("⚠️ plugins.json not found")
        return

    if force or prompt_yes_no("Are you sure you want to delete plugins.json? (y/n): "):
        try:
            os.remove("plugins.json")
            print("🗑️ Deleted plugins.json")
        except Exception as e:
            print(f"❌ Failed to delete plugins.json: {e}")


def remove_json_entry(name):
    plugins = load_plugins()
    if not plugins:
        print("⚠️ No plugins found in plugins.json")
        return
    remove_plugin_from_json(plugins, name)
