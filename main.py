import argparse
from add import add_plugin
from install import install_plugins, install_single_plugin
from sync import sync_plugins
from edit import edit_plugin
from clean import cleanup_plugins
from backup import create_backup, clear_backups
from remove import remove_plugins, delete_plugins_json, remove_json_entry


def main():
    parser = argparse.ArgumentParser(description="Neovim Plugin Manager")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add an entry to 'plugins.json' to be installed")
    add_parser.add_argument("repo", help="Plugin in the format 'author/name'")
    add_parser.add_argument("--install", action="store_true", help="Install plugin")
    add_parser.add_argument("--plugin-type", choices=["start","opt"], default="start")
    add_parser.add_argument("--tag", help="Optional tag")
    add_parser.add_argument("--branch", help="Optional branch")
    add_parser.add_argument("--build", nargs="+", help="Post install build step(s)")

    install_parser = subparsers.add_parser("install", help="Install plugin(s) in plugins.json with confirmation for each plugin")
    install_parser.add_argument("names", nargs="*", help="Install specific plugin(s)")
    install_parser.add_argument("--force", action="store_true", help="Install all orphaned plugins without confirmation")
    install_parser.add_argument("--dry-run", action="store_true", help="Show plugin(s) to be installed")

    sync_parser = subparsers.add_parser("sync", help="Sync plugins from disk to plugins.json")
    sync_parser.add_argument("--force", action="store_true")

    backup_parser = subparsers.add_parser("backup", help="Create backup of plugin config files")
    backup_parser.add_argument("--init", action="store_true", help="Backup init.lua")
    backup_parser.add_argument("--json", action="store_true", help="Backup plugins.json")
    backup_parser.add_argument("--plugins", action="store_true", help="Backup lua/plugins")
    backup_parser.add_argument("--core", action="store_true", help="Backup lua/core")

    edit_parser = subparsers.add_parser("edit", help="Edit a plugin in plugins.json")
    edit_parser.add_argument("name", help="Name of the plugin to edit")
    edit_parser.add_argument("--repo", help="New repo URL")
    edit_parser.add_argument("--plugin-type", choices=["start", "opt"], help="Lazy load?")
    edit_parser.add_argument("--tag", help="Tag to use")
    edit_parser.add_argument("--branch", nargs="+", help="Branch to use")
    edit_parser.add_argument("--build", nargs="+", help="Build step(s) after install")
    edit_parser.add_argument("--add-build", nargs="+", help="Build step(s) after install")
    edit_parser.add_argument("--remove-build", nargs="+", help="Remove build step(s) after install")
    edit_parser.add_argument("--clear-tag", action="store_true", help="Remove the tag field")
    edit_parser.add_argument("--clear-branch", action="store_true", help="Remove the branch field")
    edit_parser.add_argument("--clear-build", action="store_true", help="Remove build step(s)")
    edit_parser.add_argument("--remove", action="store_true", help="Remove an entire entry from plugins.json")

    remove_parser = subparsers.add_parser("remove", help="Remove plugins from config, repo, and init.lua")
    remove_parser.add_argument("names", nargs="*", help="Name(s) of plugin(s) to remove")
    remove_parser.add_argument("--force", action="store_true", help="Skip all confirmation prompts")
    remove_parser.add_argument("--backup", action="store_true", help="Create backup before removing")
    remove_parser.add_argument("--json", action="store_true", help="Remove from plugins.json")
    remove_parser.add_argument("--repo", action="store_true", help="Delete the plugin repo")
    remove_parser.add_argument("--config", action="store_true", help="Delete lua config")
    remove_parser.add_argument("--require", action="store_true", help="Remove require() from init.lua")

    cleanup_parser = subparsers.add_parser("clean", help="Remove plugins not found on disk")
    cleanup_parser.add_argument("--force", action="store_true", help="Skip confirmation prompt")
    cleanup_parser.add_argument("--dry-run", action="store_true", help="Preview changes without saving")

    delete_json_parser = subparsers.add_parser("delete-json", help="Remove plugins from config, repo, and init.lua")
    delete_json_parser.add_argument("--force", action="store_true", help="Delete plugins.json file")

    clear_parser = subparsers.add_parser("clear-backups", help="Delete backup directory")
    clear_parser.add_argument("--force", action="store_true", help="Delete backup directory without confirmation")

    args = parser.parse_args()

    if args.command == "add":
        plugin = add_plugin(
            identifier=args.repo,
            plugin_type=args.plugin_type,
            tag=args.tag,
            branch=args.branch,
            build=args.build
        )
        if args.install and plugin:
            success = install_single_plugin(plugin)
            if success:
                print(f"Installed {plugin['name']} after adding.")
    elif args.command == "install":
        install_plugins(
            names=args.names,
            force=args.force,
            dry_run=args.dry_run,
        )
    elif args.command == "sync":
        sync_plugins(force_repo_update=args.force)
    elif args.command == "backup":
        if not (args.init or args.json or args.plugins or args.core):
            create_backup()
        else:
            create_backup(
                include_init=args.init,
                include_json=args.json,
                include_plugins=args.plugins,
                include_core=args.core,
            )
    elif args.command == "edit":
        if args.remove:
            remove_json_entry(args.name)
        else:
            edit_plugin(
                name=args.name,
                repo=args.repo,
                plugin_type=args.plugin_type,
                tag=args.tag,
                branch=args.branch,
                build=args.build,
                add_build=args.add_build,
                remove_build=args.remove_build,
                clear_tag=args.clear_tag,
                clear_branch=args.clear_branch,
                clear_build=args.clear_build
            )
    elif args.command == "remove":
        remove_plugins(
            names=args.names,
            force=args.force,
            backup=args.backup,
            json=args.json,
            repo=args.repo,
            config=args.config,
            require=args.require
        )
    elif args.command == "clean":
        cleanup_plugins(force=args.force, dry_run=args.dry_run)
    elif args.command == "remove-json":
        delete_plugins_json(force=args.force)
    elif args.command == "clear-backups":
        clear_backups(force=args.force)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
