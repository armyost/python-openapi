
from flask 		import Flask
from sqlalchemy	import create_engine
from kafka 		import KafkaConsumer, KafkaAdminClient
from flask_cors import CORS

from view		import create_endpoints
from model		import *
from service	import *


class Services:
    pass

class Models:
    pass

###################################################################
# Create APP
###################################################################
	
def create_app(config_path):
    app = Flask(__name__)
    CORS(app)

    app.config.from_pyfile(config_path)

    database = create_engine(app.config['DB_URL'], encoding = 'utf-8', max_overflow = 0)
    commonBackendUrl=app.config['COMMON_BACKEND_URL']
    # kakafBroker=app.config['KAFKA_BROKER']
    # print("KAFKA BROKER ADDRESS is "+kakafBroker) ##

    # kafkaConsumer = KafkaConsumer(bootstrap_servers=kakafBroker)
    # kafkaAdminClient = KafkaAdminClient(bootstrap_servers=kakafBroker)
    
	## Persistence Layer
    model = Models
    model.APIBaseCodeDao = APIBaseCodeDao(database, commonBackendUrl)
	
	## Business Layer
    services = Services
    services.FrtlzrStdService = FrtlzrStdService(model.APIBaseCodeDao)
    services.APIBaseCodeService = APIBaseCodeService(model.APIBaseCodeDao)
    
	## 엔드포인트 생성		
    create_endpoints(app, services)

    return app