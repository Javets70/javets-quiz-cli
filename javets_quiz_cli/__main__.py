import typer 
import subprocess ,os , platform 
from rich.console import Console
from rich.prompt import Prompt
from bts import QuizCli
import json

config_path = "./QuizCli_config.json"
console = Console()
app = typer.Typer()
quiz = QuizCli()

@app.command("conf")
def configure_quizcli(help="OPEN CONFIGURATION FILE IN DEFAULT EDITOR"):
    if platform.system() == 'Darwin':
        subprocess.call(('open' , config_path ))
    elif platform.system() == 'Windows':
        os.startfile(config_path)
    else:
        subprocess.call(('xdg-open' , config_path))

@app.command('keygen')
def generate_key(help="GENERATE ENCRYPTION KEY"):
    quiz.gen_key()
    console.print(f'[bold red]\nTHE ENCRYPTION KEY HAS BEEN SAVED IN "user.key" \
                    \nYOU MUST NOT SHARE THIS KEY WITH ANYONE \nYOUR KEY IS [u]{ quiz.user_key} [/] ')

@app.command('edit')
def edit_file(file_path = typer.Argument(...) , help = "OPEN THE GIVEN FILE PATH FOR EDITING" ):
    if platform.system() == 'Darwin':
        subprocess.call(["open" , file_path])
    elif platform.system() == 'Windows':
        os.startfile(file_path)
    else:
        subprocess.call("xdg-open" , file_path)

@app.command('encrypt')
def encrypt_files(user_key = typer.Argument('None' , help="ENTER THE KEY TO ENCRYPT THE FILES")):
    user_input = Prompt.ask("[bold red]\nStarting this will remove the original files and create the newly encrypted files.\
                         \nDo you wish to continue? " , choices=['yes' , 'y' , 'no' , 'n'])
    if user_input in ['yes' , 'y']:  
        path1 = console.input("Enter the path to the [bold underline]questions[/] file : ")
        path2 = console.input("Enter the path to the [bold underline]answers file[/] : ")
    else:
        raise typer.Exit()
    if not os.path.isfile(path1):
        console.print(f"File at {path1} not found , please check your path")
        raise typer.Exit()
    elif not os.path.isfile(path2):
        console.print(f"File at {path2} not found , please check your path")
        raise typer.Exit()
    elif os.path.isfile(user_key):
        user_key = open(user_key).read().replace('\n' , '').read()
    else:  
        quiz.encrypt_data(path1 , user_key)
        quiz.encrypt_data(path2 , user_key)  
        os.remove(path1)
        os.remove(path2)
        config = json.loads(open('./QuizCli/config.json').read())
        path1 = './QuizCli/' +"_encrypted_" +  os.path.basename(path1)
        path2 = './QuizCli/' +"_encrypted_" +  os.path.basename(path2)
        config['path1'] = path1
        config['path2'] = path2
        json.dump(config , open('./QuizCli/config.json' , 'w'))
        console.print("[bold green]\n\nYOU CANT START THE QUIZ NOW")

@app.command('start')
def start_quiz(user_key = typer.Argument('None' , help="ENTER THE KEY TO DECRYPT THE FILES")):
    if user_key == 'None' and not os.path.isfile('./QuizCli/user.key'):
        console.print('[bold red]user.key doesnt exist ,\
        \nrun the keygen command to generate a key')
        raise typer.Exit()

    encrypted_file_count = 0
    for file_name in os.listdir('./QuizCli/'):
        if "_encrypted_" in file_name:
            encrypted_file_count += 1

    if encrypted_file_count < 2:
        console.print("[bold red]\nToo less files to work with , run encrypt command to make new encrypted files")
        raise typer.Exit()

    elif os.path.isfile(user_key):
        user_key = open(user_key).read().replace("\n" , "")
    
    config = json.loads(open('./QuizCli/config.json').read())
    ques_file = config['path1'] 
    ans_file = config['path2']
    config['+points'] = int(config['+points'])
    config['-points'] = int(config['-points'])
    raw_data1 = quiz.decrypt_data(ques_file , user_key)
    raw_data2 = quiz.decrypt_data(ans_file , user_key)

    data1 = quiz.filter_data(raw_data1)
    data2 = quiz.filter_data(raw_data2)

    points = 0
    for index ,question in enumerate(data1):
        question = question.replace("\n" , "")
        user_ans = Prompt.ask(question)
        if user_ans.lower() == data2[index].replace("\n","").lower():
            points += config['+points']
        else:
            points -= config['-points']
    console.print(f"Your score is {points}")
        

if __name__ == "__main__":
    app()


    
    
    
    



