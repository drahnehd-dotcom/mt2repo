# -*- coding: utf-8 -*-
import os
ip = "91.134.5.194"
SERVERS = {
	"live": {
		"name": "KowalMT2",
		"ip": ip,
		"mark_port": 31003,
		"mark_path": "10",
		"channels": [
			{
				"name": "CH1",
				"ip": ip,
				"port": 31003,
				"auth_port": 31001,
			},
			{
				"name": "CH2",
				"ip": ip,
				"port": 31015,
				"auth_port": 31001,
			},
			{
				"name": "CH3",
				"ip": ip,
				"port": 31027,
				"auth_port": 31001,
			},
			{
				"name": "CH4",
				"ip": ip,
				"port": 31039,
				"auth_port": 31001,
			},
			{
				"name": "CH5",
				"ip": ip,
				"port": 31051,
				"auth_port": 31001,
			},
		]
	},

	"dev": {
		"name": "DEV Server",
		"ip": "localhost",
		"mark_port": 31003,
		"mark_path": "10",
		"channels": [
			{
				"name": "CH1",
				"ip": "localhost",
				"port": 31003,
				"auth_port": 31001,
			},
		]
	},
}


def is_dev_mode_available() -> bool:
	return os.path.exists("dev") or os.path.exists("dev.txt")


def get_server(environment: str = "live") -> dict:
	return SERVERS.get(environment, SERVERS["live"])


def get_channels(environment: str = "live") -> list:
	server = get_server(environment)
	return server.get("channels", [])


def get_channel_by_index(environment: str, index: int) -> dict:
	channels = get_channels(environment)
	if 0 <= index < len(channels):
		return channels[index]
	return None
