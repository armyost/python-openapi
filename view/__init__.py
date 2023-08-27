from flask      import request, jsonify, current_app, Response, g
from flask.json import JSONEncoder

def create_endpoints(app, services):
    app.json_encoder = JSONEncoder

    @app.route("/ping", methods=['GET'])
    def ping():
        return "pong"

    # 단말의 GPS 위치에 따른 시비량 추천
    @app.route("/findFrtlzrStdPnu/<group_id>", methods=['GET'])
    def findFrtlzrStdPnu(group_id):
        dicAddress = services.FrtlzrStdService.addressFind(group_id)
        endpoint_pnu = services.FrtlzrStdService.pnuCodeFind(dicAddress)
        return services.FrtlzrStdService.frtlzrStdPnuFind(endpoint_pnu)
    
    @app.route("/findFrtlzrStdPnuTop/<group_id>", methods=['GET'])
    def findFrtlzrStdPnuTop(group_id):
        dicAddress = services.FrtlzrStdService.addressFind(group_id)
        endpoint_pnu = services.FrtlzrStdService.pnuCodeFind(dicAddress)
        return services.FrtlzrStdService.frtlzrStdPnuTopFind(endpoint_pnu)
    
    # 작물에 따른 시비량 추천
    @app.route("/findCropName/<search_word>", methods=['GET'])
    def findCropName(search_word):
        return jsonify({'searchResult' : services.APIBaseCodeService.cropNameFind(search_word)})
        
    @app.route("/listCropName", methods=['GET'])
    def listCropName():
        return jsonify({'searchResult' : services.APIBaseCodeService.cropNameList()})

    @app.route("/detailFrtlzrStdCrop/<crop_name>", methods=['GET'])
    def detailFrtlzrStdCrop(crop_name):
        crop_code = services.APIBaseCodeService.cropCodeFind(crop_name)
        return services.FrtlzrStdService.frtlzrStdCropFind(crop_code)