import flet as ft
import sys
import os
import platform
from pathlib import Path
from theme import get_palette
from icons import AppIcons
from config_manager import get_config
from backup_manager import cleanup_old_backups, cleanup_orphaned_backups, verify_all_backups, get_backup_statistics

RADIUS_CARD = 12
PADDING_PAGE = 20

class SettingsView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.padding = PADDING_PAGE
        self.config = get_config()
        
        # Initialize with current palette
        self.palette = get_palette(page)
        self.bgcolor = self.palette.bg_page
        
        self.log_view = ft.ListView(
            expand=True,
            spacing=5,
            padding=10,
            auto_scroll=True,
        )
        
        # Redirect stdout to capture logs
        self.original_stdout = sys.stdout
        sys.stdout = self.LogRedirector(self.log_view)
        
        self.build_ui()

    def did_mount(self):
        pass

    def will_unmount(self):
        # Keep stdout redirected so we capture logs even when not on this view
        pass

    def update_theme(self):
        self.palette = get_palette(self.page)
        self.bgcolor = self.palette.bg_page
        self.build_ui() # Rebuild UI to update colors
        self.update()

    def build_ui(self):
        self.content = ft.Column(
            [
                ft.Text("Settings", size=28, weight=ft.FontWeight.BOLD, color=self.palette.text_main),
                ft.Container(height=20),
                
                # Backup Management Section
                self.create_backup_management_section(),
                
                ft.Container(height=15),
                
                # Top Row: Data Management + About (side by side)
                ft.Row(
                    [
                        # Data Management Section
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Data Management", size=13, weight=ft.FontWeight.BOLD, color=self.palette.text_grey),
                                    ft.Container(height=10),
                                    ft.Container(
                                        content=ft.Column(
                                            [
                                                ft.Row(
                                                    [
                                                        ft.Container(
                                                            content=ft.Icon(AppIcons.folder, size=24, color=self.palette.primary),
                                                            bgcolor=self.palette.bg_light_blue,
                                                            padding=8,
                                                            border_radius=8
                                                        ),
                                                        ft.Column(
                                                            [
                                                                ft.Text("Local data directory", size=15, weight=ft.FontWeight.W_600, color=self.palette.text_main),
                                                                ft.Text("View backup files and database", size=12, color=self.palette.text_grey),
                                                            ],
                                                            spacing=2,
                                                            alignment=ft.MainAxisAlignment.CENTER
                                                        )
                                                    ],
                                                    spacing=15
                                                ),
                                                ft.Container(height=20),
                                                ft.Container(
                                                    content=ft.Text("Open folder", size=13, color=self.palette.primary, weight=ft.FontWeight.BOLD),
                                                    padding=ft.padding.symmetric(horizontal=20, vertical=10),
                                                    border_radius=8,
                                                    bgcolor=self.palette.bg_light_blue,
                                                    on_click=self.open_data_folder,
                                                    alignment=ft.alignment.center
                                                ),
                                            ],
                                            spacing=0,
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                        ),
                                        padding=20,
                                        bgcolor=self.palette.bg_card,
                                        border_radius=RADIUS_CARD,
                                        height=170,
                                        shadow=ft.BoxShadow(
                                            spread_radius=0,
                                            blur_radius=10,
                                            color=self.palette.shadow,
                                            offset=ft.Offset(0, 4),
                                        ),
                                    ),
                                ],
                                spacing=0
                            ),
                            expand=True
                        ),
                        
                        # About Section
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("About", size=13, weight=ft.FontWeight.BOLD, color=self.palette.text_grey),
                                    ft.Container(height=10),
                                    ft.Container(
                                        content=ft.Column(
                                            [
                                                ft.Row(
                                                    [
                                                        ft.Icon(ft.Icons.INFO_OUTLINE, size=20, color=self.palette.primary),
                                                        ft.Text("Antigravity Manager", size=15, weight=ft.FontWeight.BOLD, color=self.palette.text_main),
                                                    ],
                                                    spacing=10
                                                ),
                                                ft.Container(height=15),
                                                ft.Row(
                                                    [
                                                        ft.Text("Author:", size=13, color=self.palette.text_grey, weight=ft.FontWeight.W_500),
                                                        ft.Text("TrungNguyen", size=13, color=self.palette.text_main),
                                                    ],
                                                    spacing=5
                                                ),
                                                ft.Container(height=8),
                                                ft.Row(
                                                    [
                                                        ft.Text("Official WeChat account:", size=13, color=self.palette.text_grey, weight=ft.FontWeight.W_500),
                                                        ft.Text("TrungNguyen", size=13, color=self.palette.text_main),
                                                    ],
                                                    spacing=5
                                                ),
                                            ],
                                            spacing=0,
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                        ),
                                        padding=20,
                                        bgcolor=self.palette.bg_card,
                                        border_radius=RADIUS_CARD,
                                        height=170,
                                        shadow=ft.BoxShadow(
                                            spread_radius=0,
                                            blur_radius=10,
                                            color=self.palette.shadow,
                                            offset=ft.Offset(0, 4),
                                        ),
                                    ),
                                ],
                                spacing=0
                            ),
                            expand=True
                        ),
                    ],
                    spacing=15,
                ),
                
                ft.Container(height=20),
                
                # Logs Section (takes up remaining space)
                ft.Text("System Log", size=13, weight=ft.FontWeight.BOLD, color=self.palette.text_grey),
                ft.Container(height=10),
                ft.Container(
                    content=self.log_view,
                    bgcolor="#1E1E1E", # Console always dark
                    border_radius=RADIUS_CARD,
                    expand=True,  # This will take up all remaining vertical space
                    padding=15,
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=10,
                        color=self.palette.shadow,
                        offset=ft.Offset(0, 4),
                    )
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START
        )

    def create_backup_management_section(self):
        """Create backup management controls"""
        stats = get_backup_statistics()
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Backup Management", size=13, weight=ft.FontWeight.BOLD, color=self.palette.text_grey),
                    ft.Container(height=10),
                    ft.Container(
                        content=ft.Column(
                            [
                                # Statistics
                                ft.Row(
                                    [
                                        ft.Column(
                                            [
                                                ft.Text(str(stats["total_backups"]), size=24, weight=ft.FontWeight.BOLD, color=self.palette.primary),
                                                ft.Text("Total Backups", size=11, color=self.palette.text_grey),
                                            ],
                                            spacing=2,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                        ),
                                        ft.Container(width=1, height=40, bgcolor=self.palette.text_grey, opacity=0.2),
                                        ft.Column(
                                            [
                                                ft.Text(f"{stats['total_size_mb']:.1f} MB", size=24, weight=ft.FontWeight.BOLD, color=self.palette.primary),
                                                ft.Text("Total Size", size=11, color=self.palette.text_grey),
                                            ],
                                            spacing=2,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                ),
                                ft.Container(height=15),
                                ft.Divider(height=1, color=self.palette.text_grey, opacity=0.2),
                                ft.Container(height=10),
                                # Action Buttons
                                ft.Row(
                                    [
                                        ft.ElevatedButton(
                                            "Clean Old",
                                            icon=ft.Icons.DELETE_SWEEP,
                                            on_click=self.cleanup_old_backups,
                                            style=ft.ButtonStyle(
                                                color=self.palette.text_main,
                                                bgcolor=self.palette.bg_light_blue,
                                            )
                                        ),
                                        ft.ElevatedButton(
                                            "Verify All",
                                            icon=ft.Icons.VERIFIED,
                                            on_click=self.verify_backups,
                                            style=ft.ButtonStyle(
                                                color=self.palette.text_main,
                                                bgcolor=self.palette.bg_light_blue,
                                            )
                                        ),
                                        ft.ElevatedButton(
                                            "Import",
                                            icon=ft.Icons.DOWNLOAD,
                                            on_click=self.import_backup,
                                            style=ft.ButtonStyle(
                                                color=self.palette.text_main,
                                                bgcolor=self.palette.bg_light_blue,
                                            )
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=8,
                                    wrap=True,
                                ),
                            ],
                            spacing=5,
                        ),
                        padding=20,
                        bgcolor=self.palette.bg_card,
                        border_radius=RADIUS_CARD,
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=10,
                            color=self.palette.shadow,
                            offset=ft.Offset(0, 4),
                        ),
                    ),
                ],
                spacing=0
            ),
        )
    
    def cleanup_old_backups(self, e):
        """Clean up old backups"""
        import threading
        
        def task():
            deleted, freed = cleanup_old_backups(dry_run=False)
            cleanup_orphaned_backups()
            if deleted > 0:
                self.show_message(f"Cleaned {deleted} old backups, freed {freed / 1024 / 1024:.2f} MB")
            else:
                self.show_message("No old backups to clean")
        
        threading.Thread(target=task, daemon=True).start()
    
    def verify_backups(self, e):
        """Verify all backups"""
        import threading
        
        def task():
            valid, invalid, _ = verify_all_backups()
            self.show_message(f"Verification complete: {valid} valid, {invalid} invalid")
        
        threading.Thread(target=task, daemon=True).start()
    
    def import_backup(self, e):
        """Import backup from file"""
        import threading
        import platform
        from backup_manager import import_backup as do_import
        
        def task():
            try:
                # Use platform-specific file dialog
                if platform.system() == "Darwin":
                    # macOS
                    import subprocess
                    result = subprocess.run(
                        ["osascript", "-e", 'POSIX path of (choose file with prompt "Select Backup File" of type {"json"})'],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0:
                        import_path = result.stdout.strip()
                        if do_import(import_path):
                            self.show_message("Backup imported successfully!")
                        else:
                            self.show_message("Import failed, please check the logs.")
                elif platform.system() == "Windows":
                    # Windows - show message to manually select
                    self.show_message("Please place the backup file in Downloads folder and enter the filename:")
                else:
                    # Linux
                    self.show_message("Please place the backup file in your home directory")
            except Exception as e:
                import traceback
                error_msg = f"Import error: {str(e)}\n{traceback.format_exc()}"
                from utils import error
                error(error_msg)
                self.show_message(f"Import failed: {str(e)}")
        
        threading.Thread(target=task, daemon=True).start()
    
    def show_message(self, message):
        """Show a simple message dialog"""
        dlg = ft.AlertDialog(
            title=ft.Text("Info"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=lambda e: self.page.close(dlg))
            ]
        )
        self.page.open(dlg)
    
    def open_data_folder(self, e):
        path_to_open = os.path.expanduser("~/.antigravity-agent")
        if not os.path.exists(path_to_open):
             path_to_open = os.getcwd()
        
        path_to_open = os.path.normpath(path_to_open)
             
        if platform.system() == "Darwin":
            os.system(f"open '{path_to_open}'")
        elif platform.system() == "Windows":
            try:
                os.startfile(path_to_open)
            except Exception as e:
                print(f"Failed to open folder: {e}")
        else:
            os.system(f"xdg-open '{path_to_open}'")

    class LogRedirector:
        def __init__(self, log_view):
            self.log_view = log_view
            self.terminal = sys.stdout

        def write(self, message):
            if self.terminal:
                try:
                    self.terminal.write(message)
                except:
                    pass
            if not message.strip():
                return
                
            # Simple ANSI color parsing
            text_color = "#FFFFFF" # Default log color
            clean_message = message.strip()
            
            if "\033[32m" in message: # Green (INFO)
                text_color = "#34C759"
                clean_message = clean_message.replace("\033[32m", "").replace("\033[0m", "")
            elif "\033[33m" in message: # Yellow (WARN)
                text_color = "#FFCC00"
                clean_message = clean_message.replace("\033[33m", "").replace("\033[0m", "")
            elif "\033[31m" in message: # Red (ERR)
                text_color = "#FF3B30"
                clean_message = clean_message.replace("\033[31m", "").replace("\033[0m", "")
            elif "\033[90m" in message: # Grey (DEBUG)
                text_color = "#8E8E93"
                clean_message = clean_message.replace("\033[90m", "").replace("\033[0m", "")
            
            # Remove any remaining ANSI codes if simple parsing missed them
            if "\033[" in clean_message:
                import re
                ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
                clean_message = ansi_escape.sub('', clean_message)

            self.log_view.controls.append(
                ft.Text(
                    clean_message, 
                    font_family="Monaco, Menlo, Courier New, monospace", 
                    size=12,
                    color=text_color,
                    selectable=True
                )
            )
            
            # Only try to update if the control is attached to a page
            if self.log_view.page:
                try:
                    self.log_view.update()
                except:
                    pass

        def flush(self):
            self.terminal.flush()
