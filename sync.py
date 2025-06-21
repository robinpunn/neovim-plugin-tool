from utils import (
    load_plugins,
    save_plugins,
    get_git_repo_url,
    get_existing_plugins_by_type
)


def sync_plugins(force_repo_update=False):
    plugins = load_plugins()
    plugin_dict = {p["name"]: p for p in plugins}
    new_count = 0
    updated_count = 0

    for plugin_info in get_existing_plugins_by_type():
        name = plugin_info["name"]
        plugin_type = plugin_info["type"]
        path = plugin_info["path"]
        repo = get_git_repo_url(path)

        plugin = plugin_dict.get(name)

        if plugin is None:
            plugin_dict[name] = {
                "name": name,
                "type": plugin_type,
                "repo": repo,
            }
            new_count += 1
        else:
            updated = False
            if force_repo_update:
                plugin["repo"] = repo
                updated = True
            elif repo and "repo" not in plugin:
                plugin["repo"] = repo
                updated = True
            if plugin.get("type") != plugin_type:
                plugin["type"] = plugin_type
                updated = True
            if updated:
                updated_count += 1

    save_plugins(list(plugin_dict.values()))
    print(
        f"Sync complete. {new_count} new, {updated_count} updated plugin(s)"
    )
