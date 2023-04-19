import tools.init_database_gz as gz
import tools.init_database_zs as zs

def init_db():
    # gz: 大学城校区
    # zs: 中山校区
    gz.init_db_gz()
    zs.init_db_zs()