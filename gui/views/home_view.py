import flet as ft
import threading
import time
from datetime import datetime
from process_manager import is_process_running, start_antigravity, close_antigravity
from account_manager import add_account_snapshot, list_accounts_data, switch_account, delete_account
from db_manager import get_current_account_info
from theme import get_palette
from icons import AppIcons

RADIUS_CARD = 12
PADDING_PAGE = 20

class HomeView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.padding = PADDING_PAGE
        
        # Initialize with current palette
        self.palette = get_palette(page)
        self.bgcolor = self.palette.bg_page
        
        # Status Bar Elements
        self.status_bar = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(AppIcons.info, size=16, color=self.palette.primary),
                    ft.Text("Đang trong quá trình thử nghiệm ...", size=13, weight=ft.FontWeight.W_500, color=self.palette.primary)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor=self.palette.bg_light_blue,
            padding=ft.padding.symmetric(vertical=8, horizontal=15),
            border_radius=8,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
            on_click=self.toggle_app_status
        )
        
        # List Header Elements
        self.list_title = ft.Text("Danh sách tài khoản", size=18, weight=ft.FontWeight.BOLD, color=self.palette.text_main)
        self.stats_badge = ft.Container(
            content=ft.Text("0", size=12, color=self.palette.primary, weight=ft.FontWeight.BOLD),
            bgcolor=self.palette.bg_light_blue,
            padding=ft.padding.symmetric(horizontal=8, vertical=2),
            border_radius=10,
        )
        
        # Accounts list
        self.accounts_list = ft.Column(spacing=12, scroll=ft.ScrollMode.HIDDEN)
        self.current_email = None
        self.search_query = ""
        
        # Search field
        self.search_field = ft.TextField(
            hint_text="Search accounts by name or email...",
            prefix_icon=ft.Icons.SEARCH,
            border_radius=8,
            text_size=13,
            filled=True,
            bgcolor=self.palette.bg_card,
            border_color=ft.Colors.TRANSPARENT,
            focused_border_color=self.palette.primary,
            on_change=self.on_search_changed,
            height=45,
        )
        
        # Start status monitoring
        self.running = True

    def did_mount(self):
        self.running = True
        self.build_ui()
        self.refresh_data()
        self.monitor_thread = threading.Thread(target=self.monitor_status, daemon=True)
        self.monitor_thread.start()
        
        # 自动备份当前账号
        self.auto_backup()

    def auto_backup(self):
        def task():
            # 延迟一点时间，确保UI已加载
            time.sleep(1)
            if add_account_snapshot():
                self.refresh_data()
        threading.Thread(target=task, daemon=True).start()

    def will_unmount(self):
        self.running = False
        # Wait for monitor thread to finish
        if hasattr(self, 'monitor_thread') and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2.0)

    def update_theme(self):
        self.palette = get_palette(self.page)
        self.bgcolor = self.palette.bg_page
        
        # Update static elements
        self.list_title.color = self.palette.text_main
        self.stats_badge.bgcolor = self.palette.bg_light_blue
        self.stats_badge.content.color = self.palette.primary
        self.search_field.bgcolor = self.palette.bg_card
        self.search_field.focused_border_color = self.palette.primary
        
        # Rebuild UI or refresh data to update list items
        self.refresh_data()
        self.update()
    
    def on_search_changed(self, e):
        """Handle search query changes"""
        self.search_query = e.control.value.lower().strip()
        self.refresh_data()

    def build_ui(self):
        self.content = ft.Column(
            [
                # 1. Status Notification Bar
                self.status_bar,
                
                ft.Container(height=20),
                
                # 2. List Header with Integrated Stats
                ft.Row(
                    [
                        ft.Row(
                            [
                                self.list_title,
                                self.stats_badge
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=8
                        ),
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Icon(AppIcons.add, size=14, color="#FFFFFF"), # Always white on primary
                                    ft.Text("Backup current", size=13, color="#FFFFFF", weight=ft.FontWeight.W_600)
                                ],
                                spacing=4,
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            bgcolor=self.palette.primary,
                            padding=ft.padding.symmetric(horizontal=16, vertical=8),
                            border_radius=8,
                            on_click=self.backup_current,
                            shadow=ft.BoxShadow(
                                spread_radius=0,
                                blur_radius=8,
                                color=ft.Colors.with_opacity(0.4, self.palette.primary),
                                offset=ft.Offset(0, 2),
                            )
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                
                ft.Container(height=15),
                
                # 3. Search Bar
                self.search_field,
                
                ft.Container(height=10),

                # 4. Account List Container
                ft.Container(
                    content=self.accounts_list,
                    expand=True, # Take up remaining space
                )
            ],
        )

    def refresh_data(self):
        # Refresh current email
        info = get_current_account_info()
        if info and "email" in info:
            self.current_email = info["email"]
            
        # Refresh accounts list
        self.accounts_list.controls.clear()
        accounts = list_accounts_data()
        
        # Filter accounts based on search query
        if self.search_query:
            accounts = [
                acc for acc in accounts
                if self.search_query in acc.get('name', '').lower() or
                   self.search_query in acc.get('email', '').lower()
            ]
        
        # Update stats badge
        total_accounts = len(list_accounts_data())
        if self.search_query and len(accounts) != total_accounts:
            self.stats_badge.content.value = f"{len(accounts)}/{total_accounts} Backup"
        else:
            self.stats_badge.content.value = f"{len(accounts)} Backup"
        
        if not accounts:
            empty_message = "No matching accounts found." if self.search_query else "No backup records available."
            self.accounts_list.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(AppIcons.document, size=40, color=self.palette.text_grey),
                            ft.Container(height=10),
                            ft.Text(empty_message, color=self.palette.text_grey, size=14),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    alignment=ft.alignment.center,
                    padding=40,
                    expand=True
                )
            )
        else:
            for idx, acc in enumerate(accounts):
                is_current = (acc.get('email') == self.current_email)
                self.accounts_list.controls.append(self.create_account_row(acc, is_current))
        
        self.update()

    def format_last_used(self, iso_str):
        if not iso_str:
            return "从未 - Never"
        try:
            dt = datetime.fromisoformat(iso_str)
            return dt.strftime("%Y-%m-%d %H:%M")
        except:
            return str(iso_str).split('T')[0]

    def create_account_row(self, acc, is_current):
        return ft.Container(
            content=ft.Row(
                [
                    # Left: Avatar & Info
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Text(
                                    acc['name'][0].upper() if acc['name'] else "?", 
                                    color="#FFFFFF",
                                    weight=ft.FontWeight.BOLD,
                                    size=16
                                ),
                                width=40,
                                height=40,
                                border_radius=20,
                                bgcolor=self.palette.primary if is_current else self.palette.text_grey,
                                alignment=ft.alignment.center,
                                shadow=ft.BoxShadow(
                                    spread_radius=0,
                                    blur_radius=6,
                                    color=ft.Colors.with_opacity(0.3, self.palette.primary) if is_current else "#00000000",
                                    offset=ft.Offset(0, 2),
                                )
                            ),
                            ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Text(acc['name'], size=15, weight=ft.FontWeight.BOLD, color=self.palette.text_main),
                                            ft.Container(
                                                content=ft.Text("当前 - Current", size=10, color=self.palette.primary, weight=ft.FontWeight.BOLD),
                                                bgcolor=self.palette.bg_light_blue,
                                                padding=ft.padding.symmetric(horizontal=6, vertical=2),
                                                border_radius=4,
                                                visible=is_current
                                            )
                                        ],
                                        spacing=6,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                                    ),
                                    ft.Text(acc['email'], size=12, color=self.palette.text_grey),
                                ],
                                spacing=2,
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        ],
                        spacing=12
                    ),
                    
                    # Right: Date & Menu
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        "Last time used", 
                                        size=10, 
                                        color=self.palette.text_grey,
                                        text_align=ft.TextAlign.RIGHT
                                    ),
                                    ft.Text(
                                        self.format_last_used(acc.get('last_used')), 
                                        size=12, 
                                        color=self.palette.text_grey,
                                        weight=ft.FontWeight.W_500
                                    ),
                                ],
                                spacing=2,
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.END
                            ),
                            ft.PopupMenuButton(
                                icon=AppIcons.ellipsis,
                                icon_color=self.palette.text_grey,
                                items=[
                                    ft.PopupMenuItem(
                                        text="Switch to this account", 
                                        icon=ft.Icons.SWAP_HORIZ,
                                        on_click=lambda e, aid=acc['id']: self.switch_to_account(aid)
                                    ),
                                    ft.PopupMenuItem(
                                        text="Export backup", 
                                        icon=ft.Icons.UPLOAD_FILE,
                                        on_click=lambda e, aid=acc['id'], aname=acc['name']: self.export_account(aid, aname)
                                    ),
                                    ft.PopupMenuItem(),  # Divider
                                    ft.PopupMenuItem(
                                        text="Delete backup", 
                                        icon=ft.Icons.DELETE_OUTLINE,
                                        on_click=lambda e, aid=acc['id']: self.delete_acc(aid)
                                    ),
                                ]
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=ft.padding.symmetric(horizontal=20, vertical=12),
            bgcolor=self.palette.bg_card,
            border_radius=RADIUS_CARD,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color=self.palette.shadow,
                offset=ft.Offset(0, 2),
            ),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            on_hover=self.on_card_hover
        )

    def on_card_hover(self, e):
        # Only show shadow hover effect in light mode or if shadow is visible
        if self.palette.shadow != "#00000000":
            e.control.shadow.blur_radius = 15 if e.data == "true" else 10
            e.control.shadow.offset = ft.Offset(0, 6) if e.data == "true" else ft.Offset(0, 2)
            e.control.update()

    def monitor_status(self):
        while self.running:
            is_running = is_process_running()
            
            # Update Status Bar
            content_row = self.status_bar.content
            icon = content_row.controls[0]
            text = content_row.controls[1]
            
            if is_running:
                self.status_bar.bgcolor = self.palette.bg_light_green
                icon.name = AppIcons.check_circle
                icon.color = "#34C759"
                text.value = "Antigravity Running in the background"
                text.color = "#34C759"
            else:
                self.status_bar.bgcolor = self.palette.bg_light_red
                icon.name = AppIcons.pause_circle
                icon.color = "#FF3B30"
                text.value = "Antigravity Service has been stopped (click to start)"
                text.color = "#FF3B30"
            
            # Only update if still mounted
            if self.running and self.page:
                try:
                    self.update()
                except Exception:
                    # View was unmounted, stop monitoring
                    break
            
            time.sleep(2)

    def toggle_app_status(self, e):
        if is_process_running():
            self.stop_app(e)
        else:
            self.start_app(e)

    def show_message(self, message, is_error=False):
        dlg = ft.CupertinoAlertDialog(
            title=ft.Text("提示 - Hint"),
            content=ft.Text(message),
            actions=[
                ft.CupertinoDialogAction(
                    "确定 - Sure", 
                    is_destructive_action=is_error,
                    on_click=lambda e: self.page.close(dlg)
                )
            ]
        )
        self.page.open(dlg)

    def start_app(self, e):
        if start_antigravity():
            pass
        else:
            self.show_message("Startup failed", True)

    def stop_app(self, e):
        def close_task():
            if close_antigravity():
                pass
            else:
                pass
        threading.Thread(target=close_task, daemon=True).start()

    def backup_current(self, e):
        def backup_task():
            try:
                if add_account_snapshot():
                    self.refresh_data()
                else:
                    pass
            except Exception as e:
                import traceback
                error_msg = f"备份异常 - Backup error: {str(e)}\n{traceback.format_exc()}"
                from utils import error
                error(error_msg)
                self.show_message(f"备份错误 - Backup failure: {str(e)}", True)
        threading.Thread(target=backup_task, daemon=True).start()

    def show_confirm_dialog(self, title, content, on_confirm, confirm_text="确定 - OK", is_destructive=False):
        def handle_confirm(e):
            on_confirm()
            self.page.close(dlg)
            
        dlg = ft.CupertinoAlertDialog(
            title=ft.Text(title),
            content=ft.Text(content),
            actions=[
                ft.CupertinoDialogAction(
                    "取消", 
                    on_click=lambda e: self.page.close(dlg)
                ),
                ft.CupertinoDialogAction(
                    confirm_text, 
                    is_destructive_action=is_destructive,
                    on_click=handle_confirm
                ),
            ]
        )
        self.page.open(dlg)

    def switch_to_account(self, account_id):
        def task():
            try:
                if switch_account(account_id):
                    self.refresh_data()
                    # Optional: show success message
                    # self.show_message("切换账号成功")
                else:
                    self.show_message("Account switching failed, please check the logs.", True)
            except Exception as e:
                import traceback
                error_msg = f"Account switching error: {str(e)}\n{traceback.format_exc()}"
                from utils import error
                error(error_msg)
                self.show_message(f"An error occurred: {str(e)}", True)
        threading.Thread(target=task, daemon=True).start()

    def export_account(self, account_id, account_name):
        """Export account backup to file"""
        import platform
        from backup_manager import export_backup
        
        def task():
            try:
                # Generate default filename
                import time
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                default_filename = f"{account_name}_{timestamp}.json"
                
                # Use platform-specific file dialog
                if platform.system() == "Darwin":
                    # macOS
                    import subprocess
                    result = subprocess.run(
                        ["osascript", "-e", f'POSIX path of (choose file name with prompt "Export Backup" default name "{default_filename}")'],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0:
                        export_path = result.stdout.strip()
                        if export_backup(account_id, export_path):
                            self.show_message(f"Backup exported successfully to:\n{export_path}")
                        else:
                            self.show_message("Export failed, please check the logs.", True)
                elif platform.system() == "Windows":
                    # Windows - use default Downloads folder
                    import os
                    downloads = os.path.join(os.path.expanduser("~"), "Downloads")
                    export_path = os.path.join(downloads, default_filename)
                    if export_backup(account_id, export_path):
                        self.show_message(f"Backup exported to:\n{export_path}")
                    else:
                        self.show_message("Export failed, please check the logs.", True)
                else:
                    # Linux - use home directory
                    import os
                    export_path = os.path.join(os.path.expanduser("~"), default_filename)
                    if export_backup(account_id, export_path):
                        self.show_message(f"Backup exported to:\n{export_path}")
                    else:
                        self.show_message("Export failed, please check the logs.", True)
            except Exception as e:
                import traceback
                error_msg = f"Export error: {str(e)}\n{traceback.format_exc()}"
                from utils import error
                error(error_msg)
                self.show_message(f"Export failed: {str(e)}", True)
        
        import threading
        threading.Thread(target=task, daemon=True).start()
    
    def delete_acc(self, account_id):
        def confirm_delete():
            try:
                if delete_account(account_id):
                    self.refresh_data()
                else:
                    self.show_message("Account deletion failed, please check the logs.", True)
            except Exception as e:
                import traceback
                error_msg = f"删除异常 - Deletion error: {str(e)}\n{traceback.format_exc()}"
                from utils import error
                error(error_msg)
                self.show_message(f"Deletion mistake: {str(e)}", True)
            self.page.update()

        self.show_confirm_dialog(
            title="Confirm deletion",
            content="Are you sure you want to delete this account backup? This action cannot be undone.",
            on_confirm=confirm_delete,
            confirm_text="删除 - Delete",
            is_destructive=True
        )
