from utils import load_plugins, save_plugins, plugin_exists_in_json


def parse_repo_identifier(identifier):
    if "/" not in identifier:
        raise ValueError("❌ Repo must be in the format 'author/name'")
    return identifier.strip()


def create_plugin_entry(
    name,
    repo,
    plugin_type="start",
    tag=None,
    branch=None,
    build=None
):
    entry = {
        "name": name,
        "repo": repo,
        "type": plugin_type
    }
    if build:
        entry["build"] = build if len(build) > 1 else build[0]
    if tag:
        entry["tag"] = tag
    if branch:
        entry["branch"] = branch
    return entry


def add_plugin(
    identifier,
    plugin_type="start",
    tag=None,
    branch=None,
    build=None
):
    try:
        repo = parse_repo_identifier(identifier)
    except ValueError as e:
        print(f"❌ Error: {e}")
        return

    if tag and branch:
        print("❌ Error: you can't have both a tag and a branch")
        return

    name = repo.split("/")[-1]

    plugins = load_plugins()
    if plugin_exists_in_json(plugins, name):
        print(f"⚠️ Plugin '{name}' already exists in plugins.json")
        return

    new_plugin = create_plugin_entry(name, repo, plugin_type, tag, branch, build)
    plugins.append(new_plugin)
    save_plugins(plugins)

    print(f"✅ Added plugin '{name}' ({repo}) to plugins.json")
    print("⚠️ Do not run clean before installing or this addition will be removed")

    return new_plugin
