import pandas as pd
import pymongo 
from pymongo import MongoClient
import ruamel.yaml
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap as OrderedDict
from ruamel.yaml.scalarstring import LiteralScalarString as SString

def excel2Mongo(data, sever, dbname, collect_name, yml_name= "nlu"):
    client = MongoClient(sever)
    db = client[dbname]
    myCollect = db[collect_name]
    myCollect.drop()
    array = []
    docum = {}
    if yml_name == "nlu":
        intents = pd.unique(data['intent'])
        for intent in intents:
            for i in range (0,len(data)):
                if data['intent'][i] == intent:
                    array.append(data['examples'][i])     
            docum['intent'] = intent
            docum['examples'] = array
            myCollect.insert_one(docum)
            docum = {}
            array = []
        print("Đã tạo thành công dữ liệu Nlu!!!!")
    else:
        myCollect.drop()
        for index in range(0, len(data)):
            array = eval(data['steps'][index])
            docum['story'] = data['story'][index]
            docum['steps'] = array
            myCollect.insert_one(docum)
            docum = {}
        print("Đã tạo thành công dữ liệu Story!!!!")

def mongo2Yml(sever, dbname, collect_name, yml_name="nlu"):
    client = MongoClient(sever)
    db = client[dbname]
    myCollect = db[collect_name]

    yaml_ru = ruamel.yaml.YAML()
    yaml_ru.preserve_quotes = True
    yaml_ru.indent(sequence=4, offset=2)

    if yml_name == "nlu":
        intents = myCollect.find({}, {"_id": 0})
        intents_yml = OrderedDict([('version', "2.0"), ('nlu', [])])
        for intent in intents:
            example_str = '\n'.join(intent['examples'])
            intents_yml_list = OrderedDict([
                ('intent', intent['intent']),
                ('examples', SString(example_str+'\n'))
            ])
            intents_yml['nlu'].append(intents_yml_list)
        with open('./nlu_final.yml', 'w') as file:
            yaml_ru.default_flow_style = False
            yaml_ru.dump(intents_yml, file)
        print("Đã tạo file nlu_final.yml thành công !!")
    else:
        stories = myCollect.find({}, {"_id": 0})
        stories_yml = OrderedDict([('version', '2.0'), ('stories', [])])
        for story in stories:
            story_yml_node = OrderedDict([
                ('story', story['story']),
                ('steps', [])
            ])
            for step in story['steps']:
                if len(step) >= 2:
                    story_yml_node_enti = OrderedDict([
                        (list(step)[0], list(step.values())[0]),
                        (list(step)[1], [])
                    ])      
                    for val in list(step.values())[1]:
                        for key, value in val.items():
                            # for k, v in i.items():
                            story_yml_node_enti[list(step)[1]].append(OrderedDict([(key, value)]))
                    story_yml_node['steps'].append(story_yml_node_enti)
                else:
                    for key, value in step.items():
                        story_yml_node['steps'].append(OrderedDict([(key, value)]))
            stories_yml['stories'].append(story_yml_node)
        with open('./story_final.yml', 'w') as file:
            yaml_ru.default_flow_style = False
            yaml_ru.dump(stories_yml, file)
        print("Đã tạo file story_final.yml thành công")

