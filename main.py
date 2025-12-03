from dotenv import load_dotenv
from src.workflow import Workflow
import argparse
load_dotenv()

def main():
    workflow = Workflow()
    print('CHESS ENDGAME TEACHER AGENT')
    parser = argparse.ArgumentParser(description='A script that starts up the workflow for the AI Agent')
    parser.add_argument('--topic',type=str,help='The chess endgame topic you want to study')
    args = parser.parse_args()
    if(args.topic):
        topic = args.topic
        result = workflow.run(topic)
        if result.book_text_content:
            print('All the best with your learning!!')
            

    else:
        topic = input('What Endgame do you want to study?: ').strip()
        if topic.lower() in {'quit', 'exit'}:
            print('Goodbye!!')
        elif topic:
            result = workflow.run(topic)
            if result.book_text_content:
                print('All the best with your learning!!')
                


if __name__ == "__main__":
    main()