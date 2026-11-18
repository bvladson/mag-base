"""Traduz para português os modais de ajuda que apresentam e iniciam os tours.

Mesma regra dos demais scripts: trocas exatas, cada trecho uma única vez, idempotente.
"""
from pathlib import Path

HELP = Path(__file__).resolve().parent.parent / 'overlay' / 'app' / 'Domain' / 'Help' / 'Templates'

EXPLORAR = ('>I\'ll explore on my own</x-global::forms.button>', '>Vou explorar sozinho</x-global::forms.button>')
NAO_MOSTRAR = ("Don't show this again", 'Não mostrar novamente')

TROCAS = {
    'home.blade.php': [
        EXPLORAR, NAO_MOSTRAR,
        ('Your My Work dashboard brings everything that matters into focus. <br />',
         'O painel Meu Trabalho reúne tudo o que importa. <br />'),
        ('Your most important work is now front and center, organized just for you and how your brain works best.<br /><br />',
         'Seu trabalho mais importante fica em destaque, organizado do jeito que funciona melhor para você.<br /><br />'),
        ('From quick tasks to ambitious goals, everything you need is right here. This is your space to capture ideas, track progress, and celebrate wins along the way.<br />',
         'Das tarefas rápidas às metas mais ambiciosas, está tudo aqui. Este é o seu espaço para registrar ideias, acompanhar o progresso e comemorar cada conquista.<br />'),
    ],
    'dashboard.blade.php': [
        ('Leantime is built to empower your super powers and help you see your progress towards your goals.<br />',
         'O sistema foi feito para ajudar você a enxergar o progresso rumo às suas metas.<br />'),
        ('Most of us are used to creating task lists — but we’re going to ask you to think about what exactly you are trying to accomplish.<br />',
         'Estamos acostumados a criar listas de tarefas, mas aqui a proposta é pensar primeiro no que exatamente você quer alcançar.<br />'),
        ('1. Set a vision (strategy) and set your goals<br />', '1. Defina uma visão (estratégia) e suas metas<br />'),
        ('2. Define the work that will get you to those goals<br />', '2. Defina o trabalho que leva até essas metas<br />'),
        ('3. And then reach them, planning your day to day with your My Work Dashboard.<br />',
         '3. Alcance as metas, planejando o dia a dia no painel Meu Trabalho.<br />'),
    ],
    'projectDashboard.blade.php': [
        EXPLORAR, NAO_MOSTRAR,
        ('headline="Managing Projects"', 'headline="Gestão de projetos"'),
        ('Projects in Leantime are collaborative workspaces where you and your team organize, track, and deliver work efficiently. Each project serves as a container for related goals, tasks, milestones, and allows you to monitor progress in one central location. <br /><br />',
         'Projetos são espaços de trabalho colaborativos onde você e sua equipe organizam, acompanham e entregam o trabalho. Cada projeto reúne metas, tarefas e marcos relacionados e permite acompanhar o progresso em um só lugar. <br /><br />'),
        ("Whether you're managing work, school, or internal personal initiatives, Leantime projects provide the structure and tools needed to turn ideas into successful outcomes.",
         'Seja para entregas da empresa ou iniciativas internas, os projetos dão a estrutura e as ferramentas para transformar ideias em resultados.'),
    ],
    'kanban.blade.php': [EXPLORAR, NAO_MOSTRAR],
    'roadmap.blade.php': [EXPLORAR, NAO_MOSTRAR],
    'goals.blade.php': [
        EXPLORAR, NAO_MOSTRAR,
        ('headline="Goals to keep you focused"', 'headline="Metas para manter o foco"'),
        ('Goals allow you to break down your project into achievable, measurable and actionable chunks.<br />While milestones focus on execution, goals are about the metrics you want to achieve.<br/>',
         'As metas dividem o projeto em partes alcançáveis, mensuráveis e acionáveis.<br />Enquanto os marcos focam na execução, as metas tratam dos indicadores que você quer atingir.<br/>'),
        ('Each goal should have a clear objective (the thing you want to achieve) and should be easily measurable using a single metric.<br /><br />',
         'Cada meta deve ter um objetivo claro (o que você quer alcançar) e ser medida por um único indicador.<br /><br />'),
        ('Once you have a goal you can assign milestones to it to break it down into the executable tasks.<br />',
         'Depois de criar a meta, ligue marcos a ela para desdobrá-la em tarefas executáveis.<br />'),
    ],
    'wiki.blade.php': [
        ('Documentation where you can find it', 'Documentação fácil de encontrar'),
        ('Our docs allow you to write and share documentation with your team. You can create multiple spaces to organize your documentation into teams, areas or document category.<br/>',
         'Os documentos permitem escrever e compartilhar conteúdo com a equipe. Crie vários espaços para organizar a documentação por equipe, área ou categoria.<br/>'),
        ('Create documents to share knowledge, processes and procedures. You can also create a document to share a link to a file or a folder in your cloud storage.<br/>',
         'Registre conhecimento, processos e procedimentos. Um documento também pode apontar para um arquivo ou pasta no armazenamento em nuvem.<br/>'),
    ],
    'blueprints.blade.php': [
        ('<h1>Define your projects with ease</h1>', '<h1>Defina seus projetos com facilidade</h1>'),
        ('Blueprints are your chance to make sense of all the data. Leantime has a variety of tools and canvases to define your project background via Business Model Canvases, SWOT Analysis or Empathy Maps.<br /><br />',
         'Os modelos ajudam a organizar todas as informações. O sistema oferece ferramentas e canvases para definir o contexto do projeto, como Canvas de Modelo de Negócio, Análise SWOT ou Mapa de Empatia.<br /><br />'),
        ('If you don\'t know where to start we suggest you create a "Project Value Canvas". This canvas will answer the most important questions of your project:',
         'Se não souber por onde começar, crie um "Canvas de Valor do Projeto". Ele responde às perguntas mais importantes do projeto:'),
        ('Who is your customer? <br />', 'Quem é o seu cliente? <br />'),
        ('What problem are you solving?<br />', 'Que problema você está resolvendo?<br />'),
        ('What is your solution?<br />', 'Qual é a sua solução?<br />'),
        ('What benefit does your solution offer over your competitors<br />', 'Que vantagem sua solução oferece em relação aos concorrentes?<br />'),
        ('>Create a Project Value Canvas</x-global::forms.button>', '>Criar um Canvas de Valor do Projeto</x-global::forms.button>'),
    ],
}


def main() -> None:
    for nome, pares in TROCAS.items():
        path = HELP / nome
        texto = path.read_text(encoding='utf-8')
        alterado = texto
        for antigo, novo in pares:
            n = alterado.count(antigo)
            if n == 1:
                alterado = alterado.replace(antigo, novo)
            elif not (n == 0 and novo in alterado):
                raise SystemExit(f'ERRO {nome}: trecho encontrado {n} vezes: {antigo[:70]!r}')
        if alterado != texto:
            path.write_bytes(alterado.encode('utf-8'))
            print('ok', nome)
        else:
            print('já traduzido', nome)


if __name__ == '__main__':
    main()
