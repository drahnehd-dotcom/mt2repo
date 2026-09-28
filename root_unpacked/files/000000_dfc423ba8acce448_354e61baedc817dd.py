# -*- coding: utf-8 -*-
import winreg
import logging
from typing import List, Optional, Tuple


MAX_SAVED_ACCOUNTS = 5
REGISTRY_PATH = r"Software\Kowal"


class AccountManager:

	def __init__(self):
		self.registry_path = REGISTRY_PATH
		self._ensure_registry_key()

	def _ensure_registry_key(self):
		try:
			winreg.CreateKey(winreg.HKEY_CURRENT_USER, self.registry_path)
		except Exception as e:
			logging.exception(f"Failed to create registry key: {e}")

	def _read_registry_value(self, name: str, default: str = "") -> str:
		try:
			key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.registry_path, 0, winreg.KEY_READ)
			value, _ = winreg.QueryValueEx(key, name)
			winreg.CloseKey(key)
			return value if value else default
		except FileNotFoundError:
			return default
		except Exception as e:
			logging.warning(f"Failed to read registry value {name}: {e}")
			return default

	def _write_registry_value(self, name: str, value: str):
		try:
			key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.registry_path, 0, winreg.KEY_WRITE)
			winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)
			winreg.CloseKey(key)
		except Exception as e:
			logging.exception(f"Failed to write registry value {name}: {e}")

	def _delete_registry_value(self, name: str):
		try:
			key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.registry_path, 0, winreg.KEY_WRITE)
			winreg.DeleteValue(key, name)
			winreg.CloseKey(key)
		except FileNotFoundError:
			pass
		except Exception as e:
			logging.warning(f"Failed to delete registry value {name}: {e}")

	def get_saved_accounts(self) -> List[Tuple[str, str, str, str]]:
		"""Returns list of (username, environment, password, pin) tuples."""
		accounts = []

		for i in range(MAX_SAVED_ACCOUNTS):
			username = self._read_registry_value(f"Account{i}_Username")
			environment = self._read_registry_value(f"Account{i}_Environment", "live")
			password = self._read_registry_value(f"Account{i}_Password", "")
			pin = self._read_registry_value(f"Account{i}_Pin", "")

			if username:
				accounts.append((username, environment, password, pin))

		return accounts

	def save_account(self, username: str, password: str = "", pin: str = "", environment: str = "live") -> bool:
		if not username:
			return False
		accounts = self.get_saved_accounts()
		for acc_username, acc_env, acc_password, acc_pin in accounts:
			if acc_username == username and acc_env == environment:
				return False
		if len(accounts) >= MAX_SAVED_ACCOUNTS:
			return False
		for i in range(MAX_SAVED_ACCOUNTS):
			existing = self._read_registry_value(f"Account{i}_Username")
			if not existing:
				self._write_registry_value(f"Account{i}_Username", username)
				self._write_registry_value(f"Account{i}_Environment", environment)
				self._write_registry_value(f"Account{i}_Password", password)
				self._write_registry_value(f"Account{i}_Pin", pin)
				return True
		return False

	def delete_account(self, index: int) -> bool:
		if index < 0 or index >= MAX_SAVED_ACCOUNTS:
			return False

		try:
			accounts = self.get_saved_accounts()

			if index >= len(accounts):
				return False

			for i in range(MAX_SAVED_ACCOUNTS):
				self._delete_registry_value(f"Account{i}_Username")
				self._delete_registry_value(f"Account{i}_Environment")
				self._delete_registry_value(f"Account{i}_Password")
				self._delete_registry_value(f"Account{i}_Pin")

			slot = 0
			for i, (username, env, password, pin) in enumerate(accounts):
				if i != index:
					self._write_registry_value(f"Account{slot}_Username", username)
					self._write_registry_value(f"Account{slot}_Environment", env)
					self._write_registry_value(f"Account{slot}_Password", password)
					self._write_registry_value(f"Account{slot}_Pin", pin)
					slot += 1

			return True
		except Exception as e:
			logging.exception(f"Failed to delete account: {e}")
			return False

	def get_account_by_index(self, index: int) -> Optional[Tuple[str, str, str, str]]:
		accounts = self.get_saved_accounts()
		if 0 <= index < len(accounts):
			return accounts[index]
		return None
