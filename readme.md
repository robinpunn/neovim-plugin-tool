# Neovim Plugin Tool

A neovim plugin manager cli tool built with python that uses a JSON file to track plugins.

## Todo
- Add an update feature
- Add a dependency feature
- Update print statements with log function in `utils.py`

## Current status
I got lazy. I'm using lazy.nvim

## Features
- Add plugins using `author/name` format
- Optional `tag`, `branch`, and `build` steps
- Install and remove plugins from disk
- Cleanly remove plugins from:
  - plugins.json
  - plugin repository folder
  - Lua config files
  - init.lua `require()` statements
- Sync existing disk plugins into JSON
- Backup and restore your Neovim configuration components
- Edit plugin metadata directly

## Usage
Run the CLI:

```bash
python3 main.py <command> [options]
```

## Commands

### add

Add a plugin entry to `plugins.json`.

```bash
python3 main.py add author/plugin-name --install
```

Options:
- `--plugin-type` (start or opt)
- `--tag`, `--branch`, `--build`
- `--install`: install immediately after adding

### install

Install plugin(s) listed in `plugins.json`.

```bash
python3 main.py install
```

Options:
- `--force`: skip confirmation for each plugin
- `--dry-run`: show what would be installed

### remove

Remove one or more plugins by name.

```bash
python3 main.py remove plugin-one plugin-two
```

Options:
- `--force`: skip all prompts
- `--backup`: create backup before removal
- `--json`: remove from plugins.json
- `--repo`: delete the plugin repo
- `--config`: delete Lua config
- `--require`: remove require() from init.lua

If no specific flags are used, all of the above will be prompted automatically.

### edit

Modify an existing plugin entry in `plugins.json`.

```bash
python3 main.py edit plugin-name --tag stable --add-build "make install"
```

Supports:
- Replacing repo, plugin type, tag, branch
- Adding/removing/clearing build steps
- Removing plugin entry completely with `--remove`

### sync

Sync plugins found on disk back into `plugins.json`.

```bash
python3 main.py sync
```

### backup

Create a backup of your Neovim config state.

```bash
python3 main.py backup --init --json --plugins --core
```

With no flags, backs up everything.

### clean

Remove stale plugin entries from `plugins.json` that aren’t on disk.

```bash
python3 main.py clean --force
```

### clear-backups

Delete the backup directory.

```bash
python3 main.py clear-backups --force
```

### delete-json

Delete the entire `plugins.json` file.

```bash
python3 main.py delete-json --force
```

## File Structure

- `plugins.json`: Stores plugin metadata (name, repo, type, etc.)
- `lua/plugins/*.lua`: Per-plugin config files
- `init.lua`: Central Neovim config, includes plugin `require()` lines
- `site/pack/plugins/start|opt`: Installed plugin repos
- `plugin_tool/backups`: Optional backup directory


