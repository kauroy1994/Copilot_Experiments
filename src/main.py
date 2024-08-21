import gc
from agents.Agents import Knowledge_conv_agent, Judge_agent

class Copilot:

    @staticmethod
    def obtain_knowledge_representation(test_text):

        qa_agent_1 = Knowledge_conv_agent()
        text_knowledge = qa_agent_1.convert_to_knowledge(test_text)
        return text_knowledge

    @staticmethod
    def get_query_relevant_knowledge(test_query, knowledge_repr):

        llm_judge_1 = None

def main():
    """
    main method
    """

    test_text = """Roger Federer is a professional tennis player."""*90
    test_query = """Who is Roger Federer?"""

    knowledge_repr = Copilot.obtain_knowledge_representation(test_text) #step 1.
    print (knowledge_repr)
    #get_query_relevant_knowledge = Copilot.get_relevant_knowledge(test_query,knowledge_repr) #step 2.


if __name__ == '__main__':

    #clean up memory
    gc.collect()

    #start main method
    main()

