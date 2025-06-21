from utils import (
    load_plugins,
    save_plugins,
    get_orphaned_plugins,
    filter_plugins_by_name,
    prompt_yes_no
)


def cleanup_plugins(force=False, dry_run=False):
    all_plugins = load_plugins()
    to_remove, existing_names = get_orphaned_plugins(all_plugins)
    removed_count = len(to_remove)

    if removed_count == 0:
        print("Nothing to remove")
        return

    print(f"{removed_count} orphaned plugin(s) found.")
    for plugin in to_remove:
        print(f" - {plugin['name']}")

    if dry_run:
        print("\nDry run mode: No changes made.")
        return

    if not force:
        if not prompt_yes_no("Remove them from plugins.json? (y/n): "):
            print("Cleanup aborted")
            return

    cleaned_plugins = filter_plugins_by_name(all_plugins, existing_names)

    save_plugins(cleaned_plugins)
    print(f"Removed {removed_count} orphaned plugin(s) from plugins.json.")
