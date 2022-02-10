from RawDataModel import RawDataModel
from AggregateModel import AggregateModel
from AlertDataModel import AlertDataModel
from ruleengine import RuleEngine

raw_model = RawDataModel()
aggr_model = AggregateModel()
raw_model.ForEachMinuteAndDevice(aggr_model.UpdateAggregate)

alert_model = AlertDataModel()
rule_engine = RuleEngine('rules.json')
rule_engine.ExecuteRules(alert_model.CheckRule)