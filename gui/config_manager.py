# -*- coding: utf-8 -*-
"""
Configuration Manager for Antigravity Manager
Handles user preferences and application settings
"""
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

from utils import info, error, warning, get_app_data_dir

# Default configuration
DEFAULT_CONFIG = {
    "version": "1.0",
    "auto_backup_on_startup": True,
    "auto_backup_on_switch": True,
    "backup_retention_days": 30,  # Auto-delete backups older than X days (0 = never)
    "max_backups_per_account": 5,  # Keep only N most recent backups per account
    "confirm_before_delete": True,
    "confirm_before_switch": False,
    "theme_mode": "system",  # "light", "dark", "system"
    "show_notifications": True,
    "minimize_to_tray": False,
    "start_minimized": False,
    "check_updates_on_startup": True,
    "db_timeout": 30.0,
    "db_max_retries": 3,
    "process_close_timeout": 10,
    "enable_debug_logging": False,
}


class ConfigManager:
    """Manages application configuration with thread-safe operations"""
    
    def __init__(self):
        self.config_file = get_app_data_dir() / "config.json"
        self._config: Dict[str, Any] = {}
        self.load()
    
    def load(self) -> bool:
        """Load configuration from file"""
        if not self.config_file.exists():
            info("配置文件不存在，使用默认配置")
            self._config = DEFAULT_CONFIG.copy()
            return self.save()
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)
            
            # Merge with defaults (in case new settings were added)
            self._config = DEFAULT_CONFIG.copy()
            self._config.update(loaded_config)
            
            # Validate and migrate if needed
            self._validate_config()
            
            info("配置加载成功")
            return True
            
        except json.JSONDecodeError as e:
            error(f"配置文件损坏: {e}")
            # Backup corrupted file
            backup_path = self.config_file.with_suffix('.json.corrupted')
            try:
                self.config_file.rename(backup_path)
                warning(f"已将损坏文件备份至: {backup_path}")
            except:
                pass
            
            self._config = DEFAULT_CONFIG.copy()
            return self.save()
            
        except Exception as e:
            error(f"加载配置失败: {e}")
            self._config = DEFAULT_CONFIG.copy()
            return False
    
    def save(self) -> bool:
        """Save configuration to file (atomic write)"""
        temp_file = self.config_file.with_suffix('.json.tmp')
        
        try:
            # Write to temp file first
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, ensure_ascii=False, indent=2)
            
            # Atomic rename
            temp_file.replace(self.config_file)
            return True
            
        except Exception as e:
            error(f"保存配置失败: {e}")
            # Clean up temp file
            if temp_file.exists():
                try:
                    temp_file.unlink()
                except:
                    pass
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any, save_immediately: bool = True) -> bool:
        """Set configuration value"""
        self._config[key] = value
        
        if save_immediately:
            return self.save()
        return True
    
    def update(self, updates: Dict[str, Any], save_immediately: bool = True) -> bool:
        """Update multiple configuration values"""
        self._config.update(updates)
        
        if save_immediately:
            return self.save()
        return True
    
    def reset_to_defaults(self) -> bool:
        """Reset all settings to defaults"""
        self._config = DEFAULT_CONFIG.copy()
        return self.save()
    
    def _validate_config(self):
        """Validate and fix configuration values"""
        # Ensure numeric values are in valid ranges
        if self._config.get("backup_retention_days", 0) < 0:
            self._config["backup_retention_days"] = 0
        
        if self._config.get("max_backups_per_account", 1) < 1:
            self._config["max_backups_per_account"] = 1
        
        if self._config.get("db_timeout", 10) < 5:
            self._config["db_timeout"] = 5
        
        if self._config.get("db_max_retries", 1) < 1:
            self._config["db_max_retries"] = 1
        
        if self._config.get("process_close_timeout", 5) < 5:
            self._config["process_close_timeout"] = 5
        
        # Ensure theme mode is valid
        valid_themes = ["light", "dark", "system"]
        if self._config.get("theme_mode") not in valid_themes:
            self._config["theme_mode"] = "system"
    
    def export_config(self, export_path: str) -> bool:
        """Export configuration to a file"""
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, ensure_ascii=False, indent=2)
            info(f"配置已导出至: {export_path}")
            return True
        except Exception as e:
            error(f"导出配置失败: {e}")
            return False
    
    def import_config(self, import_path: str) -> bool:
        """Import configuration from a file"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
            
            # Merge with defaults
            self._config = DEFAULT_CONFIG.copy()
            self._config.update(imported_config)
            self._validate_config()
            
            if self.save():
                info(f"配置已从 {import_path} 导入")
                return True
            return False
            
        except Exception as e:
            error(f"导入配置失败: {e}")
            return False
    
    @property
    def all(self) -> Dict[str, Any]:
        """Get all configuration as dictionary"""
        return self._config.copy()


# Global config instance
_config_instance: Optional[ConfigManager] = None


def get_config() -> ConfigManager:
    """Get global configuration instance (singleton)"""
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigManager()
    return _config_instance
