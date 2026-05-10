#!/usr/bin/env python3

import sys
import os
import subprocess
import json
import re
from pathlib import Path

try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox, simpledialog
except ImportError:
    print("Error: tkinter not available")
    sys.exit(1)

class LatticeGUI:
    def __init__(self, notes_dir):
        self.notes_dir = Path(notes_dir)
        self.notes_dir.mkdir(parents=True, exist_ok=True)
        
        self.root = tk.Tk()
        self.root.title("Lattice")
        self.root.geometry("1200x800")
        
        self.setup_ui()
        self.load_notes()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        left_frame = ttk.Frame(main_frame, width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        left_frame.pack_propagate(False)
        
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        self.search_var.trace('w', self.on_search)
        
        ttk.Label(left_frame, text="Notes:").pack(anchor=tk.W, pady=(10, 5))
        
        self.notes_listbox = tk.Listbox(left_frame)
        self.notes_listbox.pack(fill=tk.BOTH, expand=True)
        self.notes_listbox.bind('<<ListboxSelect>>', self.on_note_select)
        self.notes_listbox.bind('<Double-Button-1>', self.open_note)
        
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(button_frame, text="New Note", command=self.new_note).pack(side=tk.LEFT, padx=(0, 2))
        ttk.Button(button_frame, text="Delete", command=self.delete_note).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Graph", command=self.show_graph).pack(side=tk.LEFT, padx=2)
        
        editor_frame = ttk.Frame(right_frame)
        editor_frame.pack(fill=tk.BOTH, expand=True)
        
        title_frame = ttk.Frame(editor_frame)
        title_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(title_frame, text="Title:").pack(side=tk.LEFT)
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(title_frame, textvariable=self.title_var)
        self.title_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        ttk.Label(editor_frame, text="Content:").pack(anchor=tk.W)
        
        self.content_text = scrolledtext.ScrolledText(editor_frame, wrap=tk.WORD)
        self.content_text.pack(fill=tk.BOTH, expand=True)
        
        save_frame = ttk.Frame(editor_frame)
        save_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(save_frame, text="Save", command=self.save_note).pack(side=tk.LEFT)
        ttk.Button(save_frame, text="Backlinks", command=self.show_backlinks).pack(side=tk.LEFT, padx=(5, 0))
        ttk.Button(save_frame, text="Tags", command=self.show_tags).pack(side=tk.LEFT, padx=(5, 0))
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def run_setl_command(self, command, *args):
        try:
            script_dir = Path(__file__).parent
            gui_bridge = script_dir / "gui_bridge"
            
            cmd = [str(gui_bridge), command] + list(args)
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.notes_dir)
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                self.status_var.set(f"Error: {result.stderr.strip()}")
                return None
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            return None
    
    def load_notes(self):
        self.notes_listbox.delete(0, tk.END)
        notes_output = self.run_setl_command("list")
        
        if notes_output:
            try:
                notes = json.loads(notes_output)
                for note in sorted(notes):
                    self.notes_listbox.insert(tk.END, note)
            except json.JSONDecodeError:
                lines = notes_output.split('\n')
                for line in lines:
                    line = line.strip()
                    if line:
                        self.notes_listbox.insert(tk.END, line)
    
    def on_search(self, *args):
        query = self.search_var.get().lower()
        self.notes_listbox.delete(0, tk.END)
        
        if query:
            result = self.run_setl_command("search", query)
            if result:
                try:
                    notes = json.loads(result)
                    for note in sorted(notes):
                        self.notes_listbox.insert(tk.END, note)
                except json.JSONDecodeError:
                    lines = result.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line:
                            self.notes_listbox.insert(tk.END, line)
        else:
            self.load_notes()
    
    def on_note_select(self, event):
        selection = self.notes_listbox.curselection()
        if selection:
            note_title = self.notes_listbox.get(selection[0])
            self.load_note(note_title)
    
    def load_note(self, title):
        content = self.run_setl_command("get", title)
        if content:
            self.title_var.set(title)
            self.content_text.delete('1.0', tk.END)
            self.content_text.insert('1.0', content)
            self.status_var.set(f"Loaded: {title}")
    
    def open_note(self, event):
        selection = self.notes_listbox.curselection()
        if selection:
            note_title = self.notes_listbox.get(selection[0])
            self.load_note(note_title)
    
    def save_note(self):
        title = self.title_var.get().strip()
        content = self.content_text.get('1.0', tk.END).strip()
        
        if not title:
            messagebox.showwarning("Warning", "Please enter a title")
            return
        
        result = self.run_setl_command("create", title, content)
        if result and "Error" not in result:
            self.load_notes()
            self.status_var.set(f"Saved: {title}")
        else:
            existing = self.run_setl_command("get", title)
            if existing:
                result = self.run_setl_command("edit", title, content)
                if result and "Error" not in result:
                    self.status_var.set(f"Updated: {title}")
    
    def new_note(self):
        title = simpledialog.askstring("New Note", "Enter note title:")
        if title:
            self.title_var.set(title)
            self.content_text.delete('1.0', tk.END)
            self.content_text.insert('1.0', f"# {title}\n\n")
            self.status_var.set(f"New note: {title}")
    
    def delete_note(self):
        selection = self.notes_listbox.curselection()
        if selection:
            note_title = self.notes_listbox.get(selection[0])
            if messagebox.askyesno("Confirm Delete", f"Delete note '{note_title}'?"):
                result = self.run_setl_command("delete", note_title)
                if result and "Error" not in result:
                    self.load_notes()
                    self.title_var.set("")
                    self.content_text.delete('1.0', tk.END)
                    self.status_var.set(f"Deleted: {note_title}")
    
    def show_backlinks(self):
        title = self.title_var.get().strip()
        if not title:
            messagebox.showwarning("Warning", "Please select a note")
            return
        
        result = self.run_setl_command("backlinks", title)
        if result:
            try:
                backlinks = json.loads(result)
                if backlinks:
                    msg = "Backlinks:\n\n" + "\n".join(f"• {link}" for link in sorted(backlinks))
                else:
                    msg = "No backlinks found"
                messagebox.showinfo("Backlinks", msg)
            except json.JSONDecodeError:
                messagebox.showinfo("Backlinks", result or "No backlinks found")
    
    def show_tags(self):
        title = self.title_var.get().strip()
        if not title:
            messagebox.showwarning("Warning", "Please select a note")
            return
        
        content = self.content_text.get('1.0', tk.END)
        tags = re.findall(r'#(\w+)', content)
        
        if tags:
            msg = f"Tags in '{title}':\n\n" + "\n".join(f"• #{tag}" for tag in sorted(set(tags)))
        else:
            msg = "No tags found"
        messagebox.showinfo("Tags", msg)
    
    def show_graph(self):
        graph_window = tk.Toplevel(self.root)
        graph_window.title("Note Graph")
        graph_window.geometry("600x400")
        
        graph_text = scrolledtext.ScrolledText(graph_window, wrap=tk.WORD)
        graph_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        result = self.run_setl_command("graph")
        if result:
            try:
                graph_data = json.loads(result)
                output = "Note Graph:\n\n"
                
                if "nodes" in graph_data:
                    output += "Nodes:\n"
                    for node in graph_data["nodes"]:
                        output += f"  • {node.get('label', node.get('id', 'Unknown'))}\n"
                
                if "edges" in graph_data:
                    output += "\nEdges:\n"
                    for edge in graph_data["edges"]:
                        output += f"  {edge.get('from', '?')} → {edge.get('to', '?')}\n"
                
                if "tags" in graph_data:
                    output += "\nTags:\n"
                    for tag_info in graph_data["tags"]:
                        tag = tag_info.get('tag', 'Unknown')
                        notes = tag_info.get('notes', [])
                        output += f"  #{tag}: {', '.join(notes)}\n"
                
                graph_text.insert('1.0', output)
            except json.JSONDecodeError:
                graph_text.insert('1.0', result or "No graph data available")
        else:
            graph_text.insert('1.0', "No graph data available")
    
    def run(self):
        self.root.mainloop()

def main():
    if len(sys.argv) < 2:
        print("Usage: gui.py <notes_dir>")
        sys.exit(1)
    
    notes_dir = sys.argv[1]
    app = LatticeGUI(notes_dir)
    app.run()

if __name__ == "__main__":
    main()
