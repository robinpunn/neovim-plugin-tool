from utils import (
    load_plugins,
    get_orphaned_plugins,
    normalize_plugin_name,
    filter_plugins_by_name,
    check_if_repo_dir_exists,
    prompt_yes_no,
    PLUGIN_DIR,
    LUA_PLUGINS_DIR,
    INIT_LUA_FILE
)
import subprocess
import os


def install_plugins(names=None, force=False, dry_run=False):
    all_plugins = load_plugins()

    orphaned_plugins, _ = get_orphaned_plugins(all_plugins)
    to_install = filter_plugins_by_name(orphaned_plugins, names) if names else orphaned_plugins

    if not to_install:
        print("Nothing to install.")
        return

    print(f"{len(to_install)} plugin(s) to install:")
    for plugin in to_install:
        print(f" - {plugin['name']}")

    if dry_run:
        print("\n Dry run: no plugins installed.")
        return

    for plugin in to_install:
        if not force:
            if not prompt_yes_no(f"Install {plugin['name']}? (y/n): "):
                continue

        success = install_single_plugin(plugin)
        if success:
            print(f"Installed {plugin['name']}")
        else:
            print(f"Failed to install {plugin['name']}")


def install_single_plugin(plugin):
    plugin_type = plugin.get("type", "start")
    url = f"https://github.com/{plugin['repo']}.git"
    name = plugin['name']
    target_dir = os.path.join(PLUGIN_DIR, plugin_type, name)

    if check_if_repo_dir_exists(target_dir, name):
        return False

    if not install_repo(url, target_dir):
        return False

    handle_checkout(plugin, target_dir)

    run_build_steps(plugin, cwd=target_dir)

    create_lua_file(LUA_PLUGINS_DIR, name)

    add_to_init_lua(INIT_LUA_FILE, name)

    run_help_tags()

    return True


def install_repo(url, directory):
    try:
        subprocess.run(["git", "clone", url, directory], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to clone repo: {e}")
        return False


def handle_checkout(plugin, directory):
    try:
        if plugin.get("tag"):
            subprocess.run(["git", "checkout", f"tags/{plugin['tag']}"], cwd=directory, check=True)
        elif plugin.get("branch"):
            subprocess.run(["git", "checkout", plugin['branch']], cwd=directory, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to checkout branch or tag: {e}")
        return False


def run_build_steps(plugin, cwd=None):
    build_steps = plugin.get("build")
    if not build_steps:
        print("No build steps...")
        return False

    if isinstance(build_steps, str):
        build_steps = [build_steps]

    for step in build_steps:
        step = step.strip()
        try:
            if step.startswith(":"):
                print(f"⚙️ Running Neovim command '{step}' for {plugin['name']}...")
                subprocess.run(
                    ["nvim", "--headless", "+silent", step, "+quit"],
                    cwd=cwd or ".",
                    check=True
                )
            else:
                print(f"Running shell command '{step}' for {plugin['name']}...")
                subprocess.run(step, shell=True, cwd=cwd or ".", check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Build step failed for {plugin['name']}: {e}")
            return False
    return True


def create_lua_file(directory, plugin_name):
    try:
        os.makedirs(directory, exist_ok=True)
        normalized = normalize_plugin_name(plugin_name)
        config_path = os.path.join(directory, f"{normalized}.lua")

        if not os.path.exists(config_path):
            with open(config_path, "w") as f:
                f.write(f"-- Config for {plugin_name} created as {normalized}.lua\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create config file for {plugin_name}: {e}")
        return False


def add_to_init_lua(init_lua, name):
    normalized = normalize_plugin_name(name)
    require_line = f'require("plugins.{normalized}")'
    try:
        with open(init_lua, "a+") as f:
            f.seek(0)
            contents = f.read()
            if require_line not in contents:
                f.write(f"{require_line}\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to update init.lua for {name}: {e}")
        return False


def run_help_tags():
    try:
        subprocess.run(["nvim", "--headless", "+silent", ":helptags ALL", "+quit"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to generate help tags: {e}")
        return False


