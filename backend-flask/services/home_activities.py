from datetime import datetime, timedelta, timezone

from lib.db import pool, query_wrap_array

class HomeActivities:
  def run():
    now = datetime.now(timezone.utc).astimezone()

    sql = sql = query_wrap_array("""
      SELECT
        activities.uuid,
        users.display_name,
        users.handle,
        activities.message,
        activities.replies_count,
        activities.reposts_count,
        activities.likes_count,
        activities.reply_to_activity_uuid,
        activities.expires_at,
        activities.created_at
      FROM public.activities
      LEFT JOIN public.users ON users.uuid = activities.user_uuid
      ORDER BY activities.created_at DESC
      """)
    
    with pool.connection() as connection:
      with connection.cursor() as cursor:
        cursor.execute(sql)
        json = cursor.fetchone()
    return json[0]