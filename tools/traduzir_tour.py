"""Traduz para português os tours guiados (Shepherd) compilados no bundle JS.

Os 38 passos são localizados pelo trecho exato {id:"…",title:"…",text:…} (listado por
listar_tour.py) e substituídos na ordem em que aparecem; cada trecho precisa ocorrer uma
única vez. Idempotente: se o bundle já estiver traduzido, não altera nada.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
BUNDLE = TOOLS.parent / 'overlay' / 'public' / 'dist' / 'js' / 'compiled-app.3.10.0.min.js'
URL = '"+leantime.appUrl+"'

# (id, título, texto) na ordem do bundle. Textos são expressões JS entre aspas duplas.
PT = [
    ('welcome-step', '👋 Bem-vindo ao tour do Painel',
     '"Vamos começar pelo básico para você se situar na navegação e nos principais elementos do sistema."'),
    ('top-nav-step', 'Modos de trabalho',
     '"A barra superior mostra o \'modo de trabalho\' em que você está: dentro de um projeto, na sua área pessoal ou no modo empresa."'),
    ('menu-step', 'Menu lateral',
     '"O menu lateral detalha o modo de trabalho atual e dá acesso às diferentes áreas. Tudo o que aparece aqui pertence ao modo de trabalho selecionado acima."'),
    ('my-menu', 'Sua barra de perfil', '"Aqui ficam os links da sua conta e as notificações."'),
    ('dashboard-widgets', 'Widgets do painel',
     '"Seu painel é dividido em widgets que mostram informações focadas no seu trabalho."'),
    ('dashboard-widgets-dandd', 'Personalize seu painel',
     '"Os widgets podem ser redimensionados e reposicionados arrastando e soltando."'),
    ('my-todo-widget', 'Minhas tarefas',
     '"O widget Minhas Tarefas mostra todas as tarefas atribuídas a você no momento."'),
    ('my-todo-widget2', 'Agrupar tarefas',
     '"Use os menus aqui para filtrar suas tarefas por projeto ou agrupá-las por prioridade, status, projeto ou datas."'),
    ('my-todo-widget4', 'Ordenar tarefas',
     '"Cada tarefa pode ser arrastada para mudar a ordem. Você também pode arrastar uma tarefa para o calendário para agendá-la."'),
    ('my-todo-widget-timer', 'Inicie o cronômetro',
     '"Quando for começar a trabalhar em uma tarefa, clique no botão de iniciar o cronômetro."'),
    ('my-todo-widget-complete', 'Conclua uma tarefa',
     '"Quando a tarefa estiver pronta, marque-a como concluída pelo menu de status."'),
    ('my-todo-widget-add', 'Adicione mais tarefas',
     '"Adicione tarefas pelo botão + de cada seção ou pelo menu de 3 pontos ao lado de cada tarefa."'),
    ('finish', 'Parabéns!',
     f'"Você concluiu o tour do painel Meu Trabalho. Acesse <a href=\'{URL}/dashboard/show\'>seu projeto</a> para conhecer a gestão de projetos."'),
    ('left-nav', 'Menu do projeto',
     '"O menu do projeto organiza o projeto em seções: <strong>Sala de Arquivos</strong> - para guardar arquivos e informações, <strong>Pensar</strong> - para planejar estratégias, ideias e definições, <strong>Fazer</strong> - para gerenciar metas, marcos e tarefas."'),
    ('project-selector', 'Seletor de projetos',
     '"Use o seletor de projetos para alternar entre projetos. O menu lateral mostra tudo o que pertence ao projeto atual."'),
    ('project-checklist', 'Checklist',
     '"O checklist do projeto é uma referência rápida para ver se o projeto tem todas as informações necessárias para uma boa execução."'),
    ('project-status', 'Atualizações rápidas de status',
     '"Use as atualizações de status para compartilhar rapidamente o andamento do projeto com a equipe, usando as cores vermelho, amarelo e verde. O status fica visível em todo o sistema."'),
    ('project-progress', 'Progresso',
     '"O indicador de progresso mostra quanto do trabalho já foi concluído. Ele considera o tamanho das tarefas, a velocidade da equipe e os marcos do projeto."'),
    ('latest-tasks', 'Tarefas recentes',
     '"A lista de tarefas recentes mostra as últimas tarefas adicionadas ao projeto e pode ser usada como caixa de entrada do projeto."'),
    ('teams', 'Equipe', '"O quadro da equipe mostra os membros deste projeto."'),
    ('finished', 'Parabéns!',
     f'"Você concluiu o tour do painel do projeto. Acesse as <a href=\'{URL}/tickets/showKanban\'>Tarefas</a> para conhecer as formas de gerenciar seu trabalho."'),
    ('kanban-overview', 'Seu quadro Kanban',
     '"Este é o seu quadro Kanban. Ele ajuda a visualizar o trabalho e a limitar o que está em andamento."'),
    ('kanban-columns', 'Fluxo de trabalho',
     '"As tarefas avançam da esquerda para a direita. Arraste os cartões para atualizar o status."'),
    ('kanban-columns2', 'Colunas flexíveis',
     '"Pelo menu de 3 pontos você pode adicionar, remover e renomear colunas."'),
    ('kanban-filter', 'Filtrar tarefas',
     '"Filtre as tarefas por campos como prioridade, status, projeto ou datas."'),
    ('kanban-group', 'Raias',
     '"Você também pode agrupar as tarefas em raias no Kanban, para visualizar o trabalho por membro da equipe, prioridade ou marco."'),
    ('kanban-sprints', 'Sprints',
     '"Se você trabalha em sprints, use este menu para selecionar, criar e atualizar sprints."'),
    # O original apontava o link "Milestones" para o Kanban; aqui aponta para os marcos.
    ('kanban-congrats', 'Parabéns!',
     f'"Você concluiu o tour do Kanban. Acesse os <a href=\'{URL}/tickets/roadmap\'>Marcos</a> para aprender a criar e gerenciar marcos."'),
    ('milestone-overview', 'Marcos',
     '"Os marcos ajudam a acompanhar as principais entregas e fases do projeto."'),
    ('milestone-drag', 'Arrastar e ordenar',
     '"Cada barra representa um marco. Você pode arrastá-las na linha do tempo, reordenar e redimensionar. Tudo o que fizer nesta tela atualiza as datas dos marcos."'),
    ('milestone-filter', 'Filtro',
     '"Você pode filtrar os marcos e também ver as tarefas que fazem parte deles."'),
    ('milestone-timeframes', 'Períodos',
     '"Mude o período da linha do tempo para ver mais meses do ano ou detalhar dia a dia."'),
    ('milestone-congrats', 'Parabéns!',
     f'"Você concluiu o tour dos marcos. Acesse as <a href=\'{URL}/goalcanvas/dashboard\'>Metas</a> para aprender a criar e gerenciar metas."'),
    ('goals-overview', 'Metas', '"As metas ajudam a acompanhar o impacto mensurável dos seus projetos."'),
    ('goal-parts', 'Objetivos e métricas',
     '"Cada meta tem um Objetivo (o que você quer alcançar) e uma Métrica (como você vai medir)."'),
    ('goal-progress', 'Progresso da meta',
     '"Conforme você atualiza as métricas, a barra de progresso mostra quanto já avançou."'),
    ('milestone-connection', 'Marcos e metas',
     '"Você pode ligar metas a marcos para acompanhar o progresso das metas pelas tarefas. Isso ajuda a identificar lacunas no planejamento."'),
    ('milestone-congrats', 'Parabéns!',
     f'"Você concluiu o tour das metas. Marcos, metas e tarefas são os blocos básicos do sistema: use-os para dividir o trabalho em partes gerenciáveis. Acesse o <a href=\'{URL}/tickets/showKanban\'>quadro Kanban</a> para revisar suas tarefas."'),
]


def main() -> None:
    passos = json.loads(subprocess.run([sys.executable, str(TOOLS / 'listar_tour.py')],
                                       capture_output=True, check=True, text=True, encoding='utf-8').stdout)
    if len(passos) != len(PT):
        raise SystemExit(f'esperados {len(PT)} passos, encontrados {len(passos)}')

    s = BUNDLE.read_text(encoding='utf-8')
    if all(p['title'] == t for p, (_, t, _) in zip(passos, PT)):
        print('tour já traduzido')
        return

    for passo, (pid, titulo, texto) in zip(passos, PT):
        if passo['id'] != pid:
            raise SystemExit(f'ordem inesperada: {passo["id"]} != {pid}')
        antigo = '{id:"%s",title:"%s",text:%s' % (passo['id'], passo['title'], passo['text_expr'])
        novo = '{id:"%s",title:"%s",text:%s' % (pid, titulo, texto)
        if s.count(antigo) != 1:
            raise SystemExit(f'{pid}: trecho encontrado {s.count(antigo)} vezes')
        s = s.replace(antigo, novo)

    BUNDLE.write_bytes(s.encode('utf-8'))
    print(f'{len(PT)} passos traduzidos')


# Outros textos em inglês do mesmo bundle (fora dos tours)
EXTRAS = [
    # Alerta do mini jogo da cobrinha escondido no Leantime
    ('alert("Congratulations! You have beaten your previous high score, which was "+t+".")',
     'alert("Parabéns! Você superou seu recorde anterior, que era de "+t+".")'),
]


def extras() -> None:
    s = BUNDLE.read_text(encoding='utf-8')
    alterado = s
    for antigo, novo in EXTRAS:
        n = alterado.count(antigo)
        if n == 1:
            alterado = alterado.replace(antigo, novo)
        elif not (n == 0 and novo in alterado):
            raise SystemExit(f'extra: trecho encontrado {n} vezes: {antigo[:60]!r}')
    if alterado != s:
        BUNDLE.write_bytes(alterado.encode('utf-8'))
        print(f'{len(EXTRAS)} texto(s) extra(s) traduzido(s)')


if __name__ == '__main__':
    main()
    extras()
