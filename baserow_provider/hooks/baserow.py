from __future__ import annotations
from typing import Any, Dict
from functools import cached_property

from baserow.client import BaserowClient 
from airflow.exceptions import AirflowException
from airflow.hooks.base import BaseHook


class BaserowHook(BaseHook):
    conn_name_attr = "baserow_conn_id"
    default_conn_name = "baserow_default"

    def __init__(self, *args, **kwargs):
        super().__init__()
        
        if not self.conn_name_attr:
            raise AirflowException("conn_name_attr is not defined")
        elif len(args) == 1:
            setattr(self, self.conn_name_attr, args[0])
        elif self.conn_name_attr not in kwargs:
            setattr(self, self.conn_name_attr, self.default_conn_name)
        else:
            setattr(self, self.conn_name_attr, kwargs[self.conn_name_attr])

        
    def _get_baserow_connection(self, url: str, token: str):
        """Returns the Baserow client."""
        
        return BaserowClient(url, token)    

    @cached_property
    def get_conn(self, conn_id=None) -> BaserowClient:

        if not conn_id:
            conn_id = getattr(self, self.conn_name_attr)
        
        conn = self.get_connection(conn_id)

        conn.extra = None 
        token = conn.get_password()
        uri = conn.get_uri()
        uri = uri.replace(f":{token}@", "")

        return self._get_baserow_connection(url=uri, token=token)

    def get_baserow_table_rows(self, table_id: int, filter: list | None = None):
        """Returns the Baserow table rows."""
        return self.get_conn.list_database_table_rows(table_id, filter=filter)
    
    def update_baserow_table_row(self, table_id: int, row_id: int, record: Dict[str, Any]) -> Dict[str, Any]:
        return self.get_conn.update_database_table_row(table_id, row_id, record=record)
