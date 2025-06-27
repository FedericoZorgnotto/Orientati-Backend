from app.database import get_db_context
from app.models import Ragazzo


def get_all_ragazzi():
    with get_db_context() as db:
        ragazzi = db.query(Ragazzo).distinct().all()
        ragazzi_list = [ragazzo for ragazzo in ragazzi if ragazzo is not None]
        return ragazzi_list
