from fastapi import HTTPException
import config

class Clear:

    def clear_cache(self):
        try:
            config.cache.clear()
            return "Clean Cache"
        except:
           raise HTTPException(status_code=400, detail='Problem in clear Cache')
