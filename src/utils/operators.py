from __future__ import annotations

__all__ = ["BaseOperator", "get_operator_func"]

from typing import TYPE_CHECKING
from abc import abstractmethod
from bpy.types import Operator
import bpy

if TYPE_CHECKING:
    from bpy.types import Context

def get_operator_func(idname: str):
    module, func = idname.split(".", 1)
    return getattr(getattr(bpy.ops, module), func)

class BaseOperator(Operator):
    @classmethod
    @abstractmethod
    def _poll(cls, context: Context) -> str | None: ...

    @abstractmethod
    def _execute(
        self, context: Context
    ) -> tuple[set[str], str] | set[str] | str | None: ...

    @classmethod
    def poll(cls, context: Context) -> bool:
        msg = cls._poll(context)
        if isinstance(msg, str):
            cls.poll_message_set(msg)
            return False
        return True

    def execute(self, context: Context) -> set[str]:  # type: ignore
        result = self._execute(context)
        if isinstance(result, str):
            _return, msg = {"CANCELLED"}, result
        elif isinstance(result, tuple):
            _return, msg = result
        elif isinstance(result, set):
            _return, msg = result, None
        else:
            _return, msg = {"FINISHED"}, None
        if msg:
            self.report({"ERROR"}, msg)
        return _return
