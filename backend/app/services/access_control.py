"""Convenience wrappers used by the access-control proof test."""
from ..security.rbac import can_access, allowed_groups

def is_blocked(role: str, group: str) -> bool:
    return not can_access(role, group)
