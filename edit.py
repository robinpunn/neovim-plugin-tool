from utils import load_plugins, save_plugins


def edit_plugin(
    name,
    repo=None,
    plugin_type=None,
    tag=None,
    branch=None,
    build=None,
    add_build=None,
    remove_build=None,
    clear_tag=None,
    clear_branch=None,
    clear_build=None
):
    plugins = load_plugins()
    found = False

    for plugin in plugins:
        if plugin["name"] == name:
            found = True
            if repo:
                plugin["repo"] = repo
                print(f"Updated repo for {name} to {repo}")
            if plugin_type in {"start", "opt"}:
                plugin["type"] = plugin_type
                print(f"Set type for {name} to {plugin_type}")
            if tag:
                plugin["tag"] = tag
                plugin.pop("branch", None)
                print(f"Set tag for {name} to {tag}")
            if branch:
                plugin["branch"] = branch
                plugin.pop("tag", None)
                print(f"Set branch for {name} to {branch}")
            if build:
                plugin["build"] = build if len(build) > 1 else build[0]
            elif add_build:
                plugin.setdefault("build", [])
                if isinstance(plugin["build"], str):
                    plugin["build"] = [plugin["build"]]
                plugin["build"].extend(step for step in add_build if step not in plugin["build"])
            elif remove_build:
                current = plugin.get("build", [])
                if isinstance(current, str):
                    current = [current]
                plugin["build"] = [step for step in current if step not in remove_build]
            elif clear_build:
                plugin.pop("build", None)
            if clear_tag:
                plugin.pop("tag", None)
                print(f"Removed tag from {name}")
            if clear_branch:
                plugin.pop("branch", None)
                print(f"Removed branch from {name}")
            if clear_build:
                plugin.pop("build", None)
                print(f"Removed build step(s) from {name}")
            break

    if not found:
        print(f"Plugin '{name}' not found.")
        return

    save_plugins(plugins)
    print(f"Updated '{name}' in plugins.json")
