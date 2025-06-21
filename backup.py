import os
import shutil
from datetime import datetime
from utils import (
    INIT_LUA_FILE,
    LUA_PLUGINS_DIR,
    LUA_PLUGINS_CORE_DIR,
    JSON_FILE,
    BACKUP_DIR,
    prompt_yes_no
)


def copy_file(src, dest, description):
    try:
        shutil.copy(src, dest)
        print(f"Backed up {description}")
        return True
    except (IOError, OSError) as e:
        print(f"❌ Failed to back up {description}: {e}")
        return False


def copy_tree(src, dest, description):
    try:
        if not os.path.exists(dest):
            shutil.copytree(src, dest)
            print(f"Backed up {description}")
        else:
            print(f"Skipped {description}: already exists in backup.")
        return True
    except (IOError, OSError) as e:
        print(f"❌ Failed to back up {description}: {e}")
        return False


def create_backup_dir(needs_lua=False):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M_%S")
    backup_path = os.path.join(BACKUP_DIR, f"backup-{timestamp}")

    os.makedirs(backup_path, exist_ok=True)
    if needs_lua:
        os.makedirs(os.path.join(backup_path, "lua"), exist_ok=True)
    return backup_path


def backup_init_file(backup_path):
    if os.path.exists(INIT_LUA_FILE):
        return copy_file(INIT_LUA_FILE, os.path.join(backup_path, "init.lua"), "init.lua")
    print("Skipped init.lua: file not found")
    return False


def backup_json_file(backup_path):
    if os.path.exists(JSON_FILE):
        return copy_file(JSON_FILE, os.path.join(backup_path, "plugins.json"), "plugins.json")
    print("Skipped plugins.json: file not found")
    return False


def backup_lua_configs(backup_path, include_plugins=True, include_core=True):
    success = True
    targets = []

    if include_plugins:
        targets.append(LUA_PLUGINS_DIR)
    if include_core:
        targets.append(LUA_PLUGINS_CORE_DIR)

    for config_dir in targets:
        if os.path.exists(config_dir):
            name = os.path.basename(config_dir)
            target = os.path.join(backup_path, "lua", name)
            if not copy_tree(config_dir, target, f"plugin configs from lua/{name}"):
                success = False
        else:
            print(f"Skipped lua/{os.path.basename(config_dir)}: directory not found")
            success = False
    return success


def create_backup(include_init=True, include_json=True, include_plugins=True, include_core=True):
    needs_lua = include_plugins or include_core
    backup_path = create_backup_dir(needs_lua=needs_lua)
    success = True

    if include_init:
        if not backup_init_file(backup_path):
            success = False

    if include_json:
        if not backup_json_file(backup_path):
            success = False

    if needs_lua:
        if not backup_lua_configs(backup_path, include_plugins, include_core):
            success = False

    if success:
        print(f"\n✅ Backup complete: {backup_path}")
    else:
        print(f"\n❌ Backup completed with error: {backup_path}")

    return success


def clear_backups(force=False):
    if not os.path.exists(BACKUP_DIR):
        print("No backups found.")
        return

    if force or prompt_yes_no("Are you sure you want to delete all backups? (y/n): "):
        try:
            shutil.rmtree(BACKUP_DIR)
            print("🗑️ All backups deleted")
        except Exception as e:
            print(f"❌ Failed to delete backups: {e}")
