class APIBaseCodeService:
    def __init__(self, APIBaseCodeDao):
        self.APIBaseCodeDao = APIBaseCodeDao

    def cropNameFind(self, search_word):
        return self.APIBaseCodeDao.selectCropName(search_word)
    
    def cropCodeFind(self, crop_name):
        return self.APIBaseCodeDao.selectCropCode(crop_name)

    def cropNameList(self):
        return self.APIBaseCodeDao.selectCropName("")
