# -*- coding: utf-8 -*-
"""
Backup Management Utilities
Handles backup cleanup, verification, and maintenance
"""
import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

from utils import info, error, warning, debug, get_app_data_dir
from config_manager import get_config


def get_backup_files() -> List[Path]:
    """Get all backup files in the backups directory"""
    backup_dir = get_app_data_dir() / "backups"
    if not backup_dir.exists():
        return []
    
    return list(backup_dir.glob("*.json"))


def get_backup_info(backup_path: Path) -> Dict:
    """Extract metadata from a backup file"""
    try:
        with open(backup_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return {
            "path": backup_path,
            "email": data.get("account_email", "Unknown"),
            "backup_time": data.get("backup_time"),
            "size": backup_path.stat().st_size,
            "created": datetime.fromtimestamp(backup_path.stat().st_ctime),
        }
    except Exception as e:
        debug(f"无法读取备份文件 {backup_path}: {e}")
        return None


def cleanup_old_backups(dry_run: bool = False) -> Tuple[int, int]:
    """
    Clean up old backups based on retention policy
    
    Args:
        dry_run: If True, only report what would be deleted without actually deleting
    
    Returns:
        Tuple of (files_deleted, space_freed_bytes)
    """
    config = get_config()
    retention_days = config.get("backup_retention_days", 30)
    
    if retention_days == 0:
        info("备份保留策略: 永久保留")
        return 0, 0
    
    cutoff_date = datetime.now() - timedelta(days=retention_days)
    backup_files = get_backup_files()
    
    files_to_delete = []
    space_to_free = 0
    
    for backup_file in backup_files:
        try:
            file_time = datetime.fromtimestamp(backup_file.stat().st_mtime)
            if file_time < cutoff_date:
                files_to_delete.append(backup_file)
                space_to_free += backup_file.stat().st_size
        except Exception as e:
            warning(f"检查文件 {backup_file} 时出错: {e}")
    
    if not files_to_delete:
        info(f"没有超过 {retention_days} 天的备份需要清理")
        return 0, 0
    
    if dry_run:
        info(f"[模拟运行] 将删除 {len(files_to_delete)} 个备份文件，释放 {space_to_free / 1024 / 1024:.2f} MB")
        for f in files_to_delete:
            debug(f"  - {f.name}")
        return len(files_to_delete), space_to_free
    
    # Actually delete files
    deleted_count = 0
    freed_space = 0
    
    for backup_file in files_to_delete:
        try:
            file_size = backup_file.stat().st_size
            backup_file.unlink()
            deleted_count += 1
            freed_space += file_size
            debug(f"已删除旧备份: {backup_file.name}")
        except Exception as e:
            error(f"删除备份文件失败 {backup_file}: {e}")
    
    if deleted_count > 0:
        info(f"清理完成: 删除了 {deleted_count} 个备份文件，释放 {freed_space / 1024 / 1024:.2f} MB")
    
    return deleted_count, freed_space


def cleanup_orphaned_backups() -> int:
    """
    Remove backup files that are not referenced in accounts.json
    
    Returns:
        Number of orphaned files deleted
    """
    from account_manager import load_accounts
    
    accounts = load_accounts()
    referenced_files = set()
    
    # Collect all referenced backup files
    for acc_data in accounts.values():
        backup_file = acc_data.get("backup_file")
        if backup_file:
            referenced_files.add(Path(backup_file).name)
    
    # Find orphaned files
    backup_files = get_backup_files()
    orphaned_files = []
    
    for backup_file in backup_files:
        if backup_file.name not in referenced_files:
            orphaned_files.append(backup_file)
    
    if not orphaned_files:
        info("没有发现孤立的备份文件")
        return 0
    
    # Delete orphaned files
    deleted_count = 0
    for backup_file in orphaned_files:
        try:
            backup_file.unlink()
            deleted_count += 1
            debug(f"已删除孤立备份: {backup_file.name}")
        except Exception as e:
            error(f"删除孤立备份失败 {backup_file}: {e}")
    
    if deleted_count > 0:
        info(f"清理完成: 删除了 {deleted_count} 个孤立备份文件")
    
    return deleted_count


def verify_all_backups() -> Tuple[int, int, List[str]]:
    """
    Verify integrity of all backup files
    
    Returns:
        Tuple of (valid_count, invalid_count, invalid_file_paths)
    """
    from db_manager import verify_backup_integrity
    
    backup_files = get_backup_files()
    valid_count = 0
    invalid_count = 0
    invalid_files = []
    
    info(f"开始验证 {len(backup_files)} 个备份文件...")
    
    for backup_file in backup_files:
        is_valid, error_msg = verify_backup_integrity(str(backup_file))
        
        if is_valid:
            valid_count += 1
            debug(f"✓ {backup_file.name}")
        else:
            invalid_count += 1
            invalid_files.append(str(backup_file))
            warning(f"✗ {backup_file.name}: {error_msg}")
    
    info(f"验证完成: {valid_count} 个有效, {invalid_count} 个无效")
    return valid_count, invalid_count, invalid_files


def get_backup_statistics() -> Dict:
    """Get statistics about backups"""
    from account_manager import load_accounts
    
    backup_files = get_backup_files()
    accounts = load_accounts()
    
    total_size = sum(f.stat().st_size for f in backup_files)
    
    # Group by email
    backups_by_email = {}
    for backup_file in backup_files:
        info_dict = get_backup_info(backup_file)
        if info_dict:
            email = info_dict["email"]
            if email not in backups_by_email:
                backups_by_email[email] = []
            backups_by_email[email].append(info_dict)
    
    return {
        "total_backups": len(backup_files),
        "total_accounts": len(accounts),
        "total_size_bytes": total_size,
        "total_size_mb": total_size / 1024 / 1024,
        "backups_by_email": backups_by_email,
        "oldest_backup": min((f.stat().st_mtime for f in backup_files), default=None),
        "newest_backup": max((f.stat().st_mtime for f in backup_files), default=None),
    }


def export_backup(account_id: str, export_path: str) -> bool:
    """
    Export a backup to a specific location
    
    Args:
        account_id: Account ID to export
        export_path: Destination path for the exported backup
    
    Returns:
        True if successful
    """
    from account_manager import load_accounts
    import shutil
    
    accounts = load_accounts()
    if account_id not in accounts:
        error(f"账号不存在: {account_id}")
        return False
    
    account = accounts[account_id]
    backup_file = account.get("backup_file")
    
    if not backup_file or not os.path.exists(backup_file):
        error(f"备份文件不存在: {backup_file}")
        return False
    
    try:
        shutil.copy2(backup_file, export_path)
        info(f"备份已导出至: {export_path}")
        return True
    except Exception as e:
        error(f"导出备份失败: {e}")
        return False


def import_backup(import_path: str, account_name: str = None) -> bool:
    """
    Import a backup from an external file
    
    Args:
        import_path: Path to the backup file to import
        account_name: Optional name for the imported account
    
    Returns:
        True if successful
    """
    from account_manager import add_account_snapshot
    from db_manager import verify_backup_integrity
    import shutil
    import uuid
    
    if not os.path.exists(import_path):
        error(f"导入文件不存在: {import_path}")
        return False
    
    # Verify backup integrity
    is_valid, error_msg = verify_backup_integrity(import_path)
    if not is_valid:
        error(f"备份文件无效: {error_msg}")
        return False
    
    # Read backup metadata
    try:
        with open(import_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        email = data.get("account_email", "Unknown")
        
        # Copy to backups directory
        backup_dir = get_app_data_dir() / "backups"
        backup_dir.mkdir(exist_ok=True)
        
        new_backup_file = backup_dir / f"{uuid.uuid4()}.json"
        shutil.copy2(import_path, new_backup_file)
        
        # Add to accounts list
        from account_manager import load_accounts, save_accounts
        accounts = load_accounts()
        
        account_id = str(uuid.uuid4())
        accounts[account_id] = {
            "id": account_id,
            "name": account_name or f"Imported_{email.split('@')[0]}",
            "email": email,
            "backup_file": str(new_backup_file),
            "created_at": datetime.now().isoformat(),
            "last_used": data.get("backup_time", datetime.now().isoformat())
        }
        
        if save_accounts(accounts):
            info(f"备份已导入: {account_name or email}")
            return True
        else:
            # Clean up if save failed
            new_backup_file.unlink()
            return False
            
    except Exception as e:
        error(f"导入备份失败: {e}")
        return False
