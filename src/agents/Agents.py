import subprocess
import json
import math
from tqdm import tqdm

def chunker(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out

class JSON_validator_agent:

    def __init__(self,config = {"model":"llama3.1","prompt": "None","n_ctx": "2048"}, validator_type = "knowledge_validator"):

        self.config = config
        self.validator_type = validator_type

    def validate(self, response):

        if self.validator_type == "knowledge_validator":
            prompt = f""" There is an error in the following JSON object

            --- OBJECT ---
            {response}

            Correct the error and return the correct JSON object using the format specified below
            Make sure to only return the corrected JSON object.

            {{"Topic": "Summary"}}
            """

            command = "ollama run "+self.config["model"]+" \""+prompt+"\""
            command_output_string = str((subprocess.run(command, capture_output = True, text=True, shell=True)).stdout)
            return command_output_string

        if self.validator_type == "judge_validator":
            prompt = f"""There is an error in the following JSON object: {response}. Correct the error and return the correct JSON object. Make sure to only do as instructed and return just the corrected JSON object."""
            command = "ollama run "+self.config["model"]+" \""+prompt+"\""
            command_output_string = str((subprocess.run(command, capture_output = True, text=True, shell=True)).stdout)
            return command_output_string.strip()

class Judge_agent:

    def __init__(self, config = {"model":"llama3.1","prompt": "None","n_ctx": "2048"}):

        self.config = config

    def judge(self, query, topic):

        if self.config["prompt"] == "None":

            default_prompt = f"""Given the following query and topic pair ({query}, {topic}), Respond with if the topic is relevant to the query using using the JSON format as follows: {{Judgement:<yes/no>}}"""

            self.config["prompt"] = default_prompt
        
        command = "ollama run "+self.config["model"]+" \""+str(self.config["prompt"])+"\""
        command_output_string = str((subprocess.run(command, capture_output = True, text=True, shell=True)).stdout)
        checker_agent_1 = JSON_validator_agent(validator_type="judge_validator")
        checked_output = checker_agent_1.validate(command_output_string)
        try:
            return topic, json.loads(checked_output)
        except:
            return topic, False #handle later

class Knowledge_conv_agent:

    def __init__(self, config = {"model":"llama3.1","prompt": "None","n_ctx": "2048"}):

        self.config = config

    def convert_chunk_to_knowledge(self, text):

        if self.config["prompt"] == "None":

            default_prompt = f""" Given the following text: 
            ---- TEXT ----    
                {text}
                
            Convert the text into a topic and summary pair.
            Make sure that the topic is sufficiently informative and the summary contains all the essential information.
            Do exactly as instructed and always make sure to respond using the following JSON format:

            {{"Topic": "Summary"}}
            """

            self.config["prompt"] = default_prompt

        command = "ollama run "+self.config["model"]+" \""+str(self.config["prompt"])+"\""
        command_output_string = str((subprocess.run(command, capture_output = True, text=True, shell=True)).stdout)
        checker_agent_1 = JSON_validator_agent()
        checked_output = checker_agent_1.validate(command_output_string)
        try:
            return json.loads('{'+(checked_output.split('{')[1]).split('}')[0]+'}')
        except:
            return False

    def convert_to_knowledge(self, text, exp_order = 8):

        n_chunks = math.floor(len(text) / int(self.config["n_ctx"])*2) + 1
        chunks = [''.join(item) for item in chunker(list(text),n_chunks)]
        
        chunks = chunks * exp_order #fix later

        knowledge = []
        for chunk in tqdm(chunks):
            knowledge.append(self.convert_chunk_to_knowledge(chunk))

        return [item for item in knowledge if item]

        