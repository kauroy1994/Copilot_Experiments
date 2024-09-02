import gc
from tqdm import tqdm
from agents.Agents import Knowledge_conv_agent, Judge_agent
from assets.Data_loader import MTSS_data_loader

class Copilot:

    @staticmethod
    def obtain_knowledge_representation(test_text):

        qa_agent_1 = Knowledge_conv_agent()
        text_knowledge = qa_agent_1.convert_to_knowledge(test_text)
        return text_knowledge

    @staticmethod
    def get_query_relevant_knowledge(test_query, knowledge_repr):

        topics = []
        for item in knowledge_repr:
            try:
                topics.append(item["Topic"])
            except:
                pass

        judgements = {}
        for topic in tqdm(topics):
            topical_judge_agent = Judge_agent()
            topic, judgement = topical_judge_agent.judge(test_query, topic)
            if judgement:
                judgements[topic] = judgement

        return judgements

def main():
    """
    main method
    """

    test_qa = MTSS_data_loader.load_symbolic_data()
    exit()
    test_text = MTSS_data_loader.load_data()[:1000]
    test_query = "What is MTSS?"
    knowledge_repr = Copilot.obtain_knowledge_representation(test_text) #step 1.
    print (knowledge_repr)
    get_query_relevant_knowledge = Copilot.get_query_relevant_knowledge(test_query,knowledge_repr) #step 2.
    print (get_query_relevant_knowledge)
    #TODO: do VDB-based retr, then apply step 1. Do Vsim-based relevancy reduction.

if __name__ == '__main__':

    #clean up memory
    gc.collect()

    #start main method
    main()

