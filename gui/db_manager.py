# -*- coding: utf-8 -*-
import sqlite3
import json
import os
import time
from datetime import datetime

# Use relative imports
from utils import info, error, warning, debug, get_antigravity_db_paths

# 需要备份的键列表
KEYS_TO_BACKUP = [
    "antigravityAuthStatus",
    "jetskiStateSync.agentManagerInitState",
]

# Database connection settings
DB_TIMEOUT = 30.0  # 30 seconds timeout
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds



def get_db_connection(db_path, max_retries=3, timeout=10.0):
    """获取数据库连接，支持重试和超时
    
    Args:
        db_path: 数据库路径
        max_retries: 最大重试次数
        timeout: 连接超时时间（秒）
    """
    import time
    
    for attempt in range(max_retries):
        try:
            # 设置超时，避免永久等待
            conn = sqlite3.connect(db_path, timeout=timeout)
            # 设置 WAL 模式以减少锁定问题
            conn.execute("PRAGMA journal_mode=WAL")
            return conn
        except sqlite3.OperationalError as e:
            error_msg = str(e)
            if "locked" in error_msg.lower():
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2  # 指数退避: 2s, 4s, 6s
                    warning(f"数据库被锁定，{wait_time}秒后重试 (尝试 {attempt + 1}/{max_retries})...")
                    time.sleep(wait_time)
                else:
                    error(f"数据库被锁定: {e}")
                    error("提示: 请确保 Antigravity 应用已完全关闭")
                    return None
            else:
                error(f"连接数据库失败: {e}")
                return None
        except sqlite3.Error as e:
            error(f"数据库错误: {e}")
            return None
        except Exception as e:
            error(f"连接数据库时发生意外错误: {e}")
            return None
    
    return None

def verify_backup_integrity(backup_file_path):
    """验证备份文件的完整性
    
    Returns:
        tuple: (is_valid, error_message)
    """
    import hashlib
    
    try:
        if not os.path.exists(backup_file_path):
            return False, "备份文件不存在"
        
        # 检查文件大小
        file_size = os.path.getsize(backup_file_path)
        if file_size == 0:
            return False, "备份文件为空"
        
        if file_size > 50 * 1024 * 1024:  # 50MB
            return False, "备份文件异常大，可能已损坏"
        
        # 尝试解析 JSON
        with open(backup_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 检查必需字段
        if not isinstance(data, dict):
            return False, "备份文件格式错误"
        
        if "account_email" not in data:
            return False, "备份文件缺少账号信息"
        
        if "backup_time" not in data:
            return False, "备份文件缺少时间戳"
        
        # 检查是否有实际数据
        has_data = any(key in data for key in KEYS_TO_BACKUP)
        if not has_data:
            return False, "备份文件不包含有效数据"
        
        return True, None
        
    except json.JSONDecodeError as e:
        return False, f"JSON 解析失败: {e}"
    except Exception as e:
        return False, f"验证失败: {e}"

def backup_account(email, backup_file_path):
    """备份账号数据到 JSON 文件，支持完整性验证"""
    db_paths = get_antigravity_db_paths()
    if not db_paths:
        error("未找到 Antigravity 数据库路径")
        return False
    
    db_path = db_paths[0]
    if not db_path.exists():
        error(f"数据库文件不存在: {db_path}")
        return False
        
    info(f"正在从数据库备份数据: {db_path}")
    conn = get_db_connection(db_path)
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        data_map = {}
        
        # 1. 提取普通键值
        for key in KEYS_TO_BACKUP:
            try:
                cursor.execute("SELECT value FROM ItemTable WHERE key = ?", (key,))
                row = cursor.fetchone()
                if row:
                    data_map[key] = row[0]
                    debug(f"备份字段: {key}")
                else:
                    debug(f"字段不存在: {key}")
            except sqlite3.Error as e:
                warning(f"读取字段 {key} 失败: {e}")
                continue
        
        # 2. 添加元数据
        data_map["account_email"] = email
        data_map["backup_time"] = datetime.now().isoformat()
        data_map["backup_version"] = "1.0"
        
        # 3. 写入临时文件
        temp_file = backup_file_path + ".tmp"
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data_map, f, ensure_ascii=False, indent=2)
            
            # 4. 验证备份完整性
            is_valid, error_msg = verify_backup_integrity(temp_file)
            if not is_valid:
                error(f"备份验证失败: {error_msg}")
                os.remove(temp_file)
                return False
            
            # 5. 原子性替换（如果旧备份存在，先备份）
            if os.path.exists(backup_file_path):
                old_backup = backup_file_path + ".old"
                if os.path.exists(old_backup):
                    os.remove(old_backup)
                os.rename(backup_file_path, old_backup)
            
            os.rename(temp_file, backup_file_path)
            
            # 6. 清理旧备份
            old_backup = backup_file_path + ".old"
            if os.path.exists(old_backup):
                os.remove(old_backup)
            
            info(f"备份成功: {backup_file_path}")
            return True
            
        except IOError as e:
            error(f"写入备份文件失败: {e}")
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return False
        
    except sqlite3.Error as e:
        error(f"数据库查询出错: {e}")
        return False
    except Exception as e:
        error(f"备份过程出错: {e}")
        import traceback
        debug(traceback.format_exc())
        return False
    finally:
        try:
            conn.close()
        except:
            pass

def restore_account(backup_file_path):
    """从 JSON 文件恢复账号数据，支持完整性验证和回滚"""
    if not os.path.exists(backup_file_path):
        error(f"备份文件不存在: {backup_file_path}")
        return False
    
    # 1. 验证备份文件完整性
    info("验证备份文件完整性...")
    is_valid, error_msg = verify_backup_integrity(backup_file_path)
    if not is_valid:
        error(f"备份文件验证失败: {error_msg}")
        return False
    
    # 2. 读取备份数据
    try:
        with open(backup_file_path, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
    except Exception as e:
        error(f"读取备份文件失败: {e}")
        return False
    
    # 3. 获取数据库路径
    db_paths = get_antigravity_db_paths()
    if not db_paths:
        error("未找到 Antigravity 数据库路径")
        return False
    
    # 4. 创建当前状态的安全备份（用于回滚）
    safety_backups = []
    for db_path in db_paths:
        if db_path.exists():
            safety_backup = str(db_path) + ".safety_backup"
            try:
                import shutil
                shutil.copy2(db_path, safety_backup)
                safety_backups.append((db_path, safety_backup))
                debug(f"创建安全备份: {safety_backup}")
            except Exception as e:
                warning(f"无法创建安全备份: {e}")
    
    # 5. 执行恢复操作
    success_count = 0
    failed = False
    
    try:
        for db_path in db_paths:
            # 主数据库
            if _restore_single_db(db_path, backup_data):
                success_count += 1
            else:
                failed = True
                break
                
            # 备份数据库 (如果存在)
            backup_db_path = db_path.with_suffix('.vscdb.backup')
            if backup_db_path.exists():
                if _restore_single_db(backup_db_path, backup_data):
                    success_count += 1
                else:
                    warning(f"恢复备份数据库失败: {backup_db_path}")
        
        # 6. 如果失败，回滚到安全备份
        if failed and safety_backups:
            error("恢复失败，正在回滚到原始状态...")
            for db_path, safety_backup in safety_backups:
                try:
                    import shutil
                    shutil.copy2(safety_backup, db_path)
                    info(f"已回滚: {db_path}")
                except Exception as e:
                    error(f"回滚失败: {e}")
            return False
        
        # 7. 清理安全备份
        if not failed:
            for _, safety_backup in safety_backups:
                try:
                    os.remove(safety_backup)
                except:
                    pass
        
        return success_count > 0
        
    except Exception as e:
        error(f"恢复过程出错: {e}")
        # 尝试回滚
        if safety_backups:
            error("正在回滚到原始状态...")
            for db_path, safety_backup in safety_backups:
                try:
                    import shutil
                    shutil.copy2(safety_backup, db_path)
                except:
                    pass
        return False

def _restore_single_db(db_path, backup_data):
    """恢复单个数据库文件，支持事务回滚"""
    if not db_path.exists():
        return False
        
    info(f"正在恢复数据库: {db_path}")
    conn = get_db_connection(db_path)
    if not conn:
        return False
        
    try:
        cursor = conn.cursor()
        restored_keys = []
        
        # 开始事务
        cursor.execute("BEGIN TRANSACTION")
        
        # 1. 恢复普通键值
        for key in KEYS_TO_BACKUP:
            if key in backup_data:
                try:
                    value = backup_data[key]
                    # 确保 value 是字符串
                    if not isinstance(value, str):
                        value = json.dumps(value)
                        
                    cursor.execute("INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)", (key, value))
                    restored_keys.append(key)
                    debug(f"恢复字段: {key}")
                except sqlite3.Error as e:
                    warning(f"恢复字段 {key} 失败: {e}")
                    # 继续处理其他字段
                    continue
        
        # 提交事务
        conn.commit()
        info(f"数据库恢复完成: {db_path} (恢复了 {len(restored_keys)} 个字段)")
        return True
        
    except sqlite3.Error as e:
        error(f"数据库写入出错: {e}")
        try:
            conn.rollback()
            info("已回滚数据库事务")
        except:
            pass
        return False
    except Exception as e:
        error(f"恢复过程出错: {e}")
        try:
            conn.rollback()
        except:
            pass
        return False
    finally:
        try:
            conn.close()
        except:
            pass


def get_current_account_info():
    """从数据库中提取当前账号信息 (邮箱等)"""
    db_paths = get_antigravity_db_paths()
    if not db_paths:
        return None
    
    db_path = db_paths[0]
    if not db_path.exists():
        return None
        
    conn = get_db_connection(db_path)
    if not conn:
        return None
        
    try:
        cursor = conn.cursor()
        
        # 1. 尝试从 antigravityAuthStatus 获取
        cursor.execute("SELECT value FROM ItemTable WHERE key = ?", ("antigravityAuthStatus",))
        row = cursor.fetchone()
        if row:
            try:
                # 尝试解析 JSON
                data = json.loads(row[0])
                if isinstance(data, dict):
                    if "email" in data:
                        return {"email": data["email"]}
                    # 有些时候可能是 token，或者其他结构，这里做一个简单的遍历查找
                    for k, v in data.items():
                        if k.lower() == "email" and isinstance(v, str):
                            return {"email": v}
            except:
                pass

        # 2. 尝试从 google.antigravity 获取
        cursor.execute("SELECT value FROM ItemTable WHERE key = ?", ("google.antigravity",))
        row = cursor.fetchone()
        if row:
            try:
                data = json.loads(row[0])
                if isinstance(data, dict) and "email" in data:
                    return {"email": data["email"]}
            except:
                pass
                
        # 3. 尝试从 antigravityUserSettings.allUserSettings 获取
        cursor.execute("SELECT value FROM ItemTable WHERE key = ?", ("antigravityUserSettings.allUserSettings",))
        row = cursor.fetchone()
        if row:
            try:
                data = json.loads(row[0])
                if isinstance(data, dict) and "email" in data:
                    return {"email": data["email"]}
            except:
                pass
                
        return None
        
    except Exception as e:
        error(f"提取账号信息出错: {e}")
        return None
    finally:
        conn.close()


