from app.models.multimodal_model import MultimodalModel
from app.services.data_processing import DataProcessor
from app.services.risk_management import RiskManager
from app.utils.ray_utils import ray_remote
import ray

@ray_remote(num_cpus=2, num_gpus=1)
class AIEngine:
    def __init__(self):
        self.model = MultimodalModel()
        self.data_processor = DataProcessor()
        self.risk_manager = RiskManager()

    async def process_query(self, query):
        parsed_query = self.parse_query(query)
        data = self.data_processor.get_data(parsed_query)
        insights = self.model.get_insights(data)
        risks = self.risk_manager.assess_risk(insights)
        return {'insights': insights, 'risks': risks}

    def parse_query(self, query):
        parsed_query = {'intent': 'analyze', 'entities': []}
        return parsed_query

    async def process_query(self, query):
        parsed_query = self.parse_query(query)
        data = self.data_processor.get_data(parsed_query)
        texts = data.get('texts', [])
        insights = self.model.get_insights(texts)
        risks = self.risk_manager.assess_risk(insights)
        return {'insights': insights, 'risks': risks}