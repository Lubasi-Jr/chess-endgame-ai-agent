from dotenv import load_dotenv
from src.workflow import Workflow
load_dotenv()

workflow = Workflow()
print('CHESS ENDGAME TEACHER AGENT')
topic = input('What Endgame do you want to study?: ').strip()

if topic.lower() in {'quit', 'exit'}:
    print('Goodbye!!')
elif topic:
    result = workflow.run(topic)
    if result.book_text_content:
        print('All the best with your learning!!')
