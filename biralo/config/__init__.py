"""Configuration module for biralo."""

from biralo.config.loader import load_config, get_config_path
from biralo.config.schema import Config

__all__ = ["Config", "load_config", "get_config_path"]
