import sys
from psycopg_pool import ConnectionPool
import os
import re
class Db:
  def __init__(self):
    self.__init_pool()
  
  def __init_pool(self):
    connection_url = os.getenv("CONNECTION_URL")
    self.pool = ConnectionPool(connection_url)

  def __query_wrap_object(self, template):
    sql = f"""
    (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
    {template}
    ) object_row);
    """
    return sql

  def __query_wrap_array(self, template):
    sql = f"""
    (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
    {template}
    ) array_row);
    """
    return sql

  def __print_psycopg2_exception(self, err):
   # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print ("\npsycopg2 ERROR:", err, "on line number:", line_num)
    print ("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print ("\nextensions.Diagnostics:", err)

    # print the pgcode and pgerror exceptions
    print ("pgerror:", err)
    print ("pgcode:", err, "\n")

  def query_commit(self, sql):
    try:
      conn = self.pool.connection()
      cur = conn.cursor()
      cur.execute(sql)
      conn.commit()
      
    except Exception as err:
      self.__print_psycopg2_exception(err)

  def query_commit_with_returning_id(self, sql, **kwargs):
    self.print_sql('commit with returning',sql)

    pattern = r"\bRETURNING\b"
    is_returning_id = re.search(pattern, sql)

    with self.pool.connection() as conn:
        cur =  conn.cursor()
        cur.execute(sql,params)
        if is_returning_id:
          returning_id = cur.fetchone()[0]
        conn.commit() 
        if is_returning_id:
          return returning_id
    except Exception as err:
      self.print_sql_err(err)

  def query_json_array(self, sql):

    wrapped_sql = self.__query_wrap_array(sql)

    with self.pool.connection() as connection:
      with connection.cursor() as cursor:
        cursor.execute(wrapped_sql)
        json = cursor.fetchone()
    return json[0]
  
  def query_json_object(self, sql):
    wrapped_sql = self.__query_wrap_object(sql)

    with self.pool.connection() as connection:
      with connection.cursor() as cursor:
        cursor.execute(wrapped_sql)
        json = cursor.fetchone()
    return json[0]


db = Db()