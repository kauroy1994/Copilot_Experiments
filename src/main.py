import gc
from agents.Agents import Knowledge_conv_agent

def main():
    """
    main method
    """

    #test QA convert agent
    qa_agent_1 = Knowledge_conv_agent()
    test_text = """Roger Federer is a professional tennis player.
    """
    text_knowledge = qa_agent_1.convert_to_knowledge(test_text)
    print (text_knowledge)

if __name__ == '__main__':

    #clean up memory
    gc.collect()

    #start main method
    main()

