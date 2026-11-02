import re
from django.core.files.storage import FileSystemStorage

class NalogeStorage(FileSystemStorage):
    """Omogoča zapis »Priimek Ime – Naslov naloge.pdf« in prepis ob potrditvi."""
    def __init__(self,*args,**kwargs):
        kwargs.setdefault('allow_overwrite',True)
        super().__init__(*args,**kwargs)
    def get_valid_name(self,name):
        return re.sub(r'[\\/:*?"<>|\x00-\x1f]','',name).strip()

def naloge_storage():
    return NalogeStorage()
