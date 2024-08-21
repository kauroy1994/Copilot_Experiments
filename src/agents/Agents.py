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

    def __init__(self,config = {"model":"llama3.1","prompt": "None","n_ctx": "2048"}):

        self.config = config

    def validate(self, response):

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

class Judge_agent:

    def __init__(self, config = {"model":"llama3.1","prompt": "None","n_ctx": "2048"}):

        self.config = config

    def judge(self, item1, item2):

        prompt = f""" none
        """

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
            return json.loads(checked_output)
        except:
            return False #handle later

    def convert_to_knowledge(self, text, max_retries = 4):

        n_chunks = math.floor(len(text) / int(self.config["n_ctx"])*2) + 1
        chunks = [''.join(item) for item in chunker(list(text),n_chunks)]
        
        chunks = chunks * max_retries #fix later

        knowledge = []
        for chunk in tqdm(chunks):
            knowledge.append(self.convert_chunk_to_knowledge(chunk))

        return [item for item in knowledge if item]

        