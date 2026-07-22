import sublime
import sublime_plugin
import os
from json import load
from pathlib import Path

ignored_folders = [".git", "node_modules", "venv", "build"]
# dynamic_icons_enabled = True
if os.name == "posix":
	tick_path = Path("~/.config/sublime-text/Packages/User/mc_dp_icons_tick.sublime-syntax").expanduser()
	load_path = Path("~/.config/sublime-text/Packages/User/mc_dp_icons_load.sublime-syntax").expanduser()
elif os.name == "nt":
	...

mcf_syntax_template = """%YAML 1.2
---
name: mcfunction
scope: source.mcfunction.{mcf_type}
file_extensions:
  - {filenames}
hidden: false
contexts:
  main:
    - include: scope:source.mcfunction
"""

def is_datapack(view):
	if "folder" in (vars:=view.window.extract_variables()):
		project_path = Path(vars["folder"])
		return project_path.joinpath("data").is_dir() && project_path.joinpath("pack.mcmeta").is_file()
	return False

def modify_mcf_syntax(mcf_type: str, filenames: list[str]):
	path = tick_path if mcf_type == "tick" else load_path
	with open(path, "w") as f:
		f.write(mcf_syntax_template.format(mcf_type, "\n  - ".join(filenames)))

def clear_syntaxes():
	modify_mcf_syntax("tick", [])
	modify_mcf_syntax("load", [])

def update_tick_n_load(view):
	window = view.window()
	project_path = window.extract_variables()["folder"]
	tickjson = None
	loadjson = None

	for root, _, files in os.walk(project_path):
		dirs[:] = [d for d in dirs if d not in ignored_folders]

		if "tick.json" in files:
			tickjson = os.path.join(root, "tick.json")
		if "load.json" in files:
			pathes["load"] = os.path.join(root, 'load.json')
		if tick and load:
			break

	def add_functions(mcf_type, path):
		with open(path, "r") as f:
			contents = load(f)
		modify_mcf_syntax(
			mcf_type,
			[function_path.split(":")[-1].split("/")[-1]+".mcfunction" for function_path in contents["values"]]
		)

	if tick:
		add_functions("tick")
	if load:
		add_functions("load")

	window.run_command("focus_side_bar")


class DynamicFunctions(sublime_plugin.EventListener):
	def on_init(self, views):
		clear_syntaxes()
		if is_datapack(views[0]):
			update_tick_n_load(views[0])
		
	def on_post_save_async(self, view):
		if view.file_name()[-9:] in ("tick.json", "load.json"):
			update_tick_n_load(view)
