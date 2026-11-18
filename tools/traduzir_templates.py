"""Traduz para português os textos fixos em inglês dos templates Blade.

Fonte dos textos: tools/inventario/templates.json (gerado por inventario_ingles.py).
Substituições seguras:
  - nó de texto inteiro: o trecho precisa estar entre ">"/"}}"/"!!}" e "<"/"{{"/"{!!"/"@";
  - atributo visível com valor exato (placeholder="…", title="…", labelText="…" …);
  - nunca dentro de <script>, <style>, @php, {{ }}, {!! !!} ou comentários Blade.
Textos com expressões no meio da frase ficam em MANUAL (pares exatos por arquivo).
Idempotente. Uso: python traduzir_templates.py
"""
import json
import re
import shutil
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
OVERLAY = TOOLS.parent / 'overlay'
ORIGINAL = Path(r'C:\Users\VLADSON\Downloads\Leantime-v3.10.0')

# Telas removidas, sem uso ou de teste: não traduzir
PULAR = (
    'app/Domain/Help/Templates/support.blade.php',
    'app/Domain/Plugins/',
    'app/Domain/Notifications/Templates/partials/latestNews.blade.php',
    'app/Views/Templates/layouts/registration.blade.php',
    'app/Domain/Tickets/Templates/componentTest.blade.php',
)

ATRIBUTOS = ('placeholder', 'title', 'alt', 'aria-label', 'data-tippy-content', 'label', 'labelText', 'headline',
             'text', 'helpText', 'caption', 'emptyText', 'tooltip', 'value', 'data-placeholder', 'subtitle')

TRAD = {
    '* the archive status is protected cannot be renamed or removed.': '* o status Arquivado é protegido e não pode ser renomeado nem removido.',
    '<strong>Keyboard Shortcuts:</strong><br>Enter: Save and close<br>Shift+Enter: Save and add another<br>Esc: Cancel':
        '<strong>Atalhos de teclado:</strong><br>Enter: salvar e fechar<br>Shift+Enter: salvar e adicionar outra<br>Esc: cancelar',
    'Account': 'Conta',
    'Activity': 'Atividade',
    'Add Milestone': 'Adicionar marco',
    'Add reaction': 'Adicionar reação',
    'Add Subtask': 'Adicionar subtarefa',
    'Add tags...': 'Adicionar etiquetas...',
    'Add To-Do': 'Adicionar tarefa',
    'Add Todo': 'Adicionar tarefa',
    'Administration': 'Administração',
    'All Clients': 'Todos os clientes',
    'All set, we are importing the data you see below.': 'Tudo certo, estamos importando os dados abaixo.',
    'All Statuses': 'Todos os status',
    'All Users': 'Todos os usuários',
    'API Access': 'Acesso à API',
    'At Risk': 'Em risco',
    'Available Integrations': 'Integrações disponíveis',
    'Available methods:': 'Métodos disponíveis:',
    'Back': 'Voltar',
    'board': 'quadro',
    'Calendars': 'Calendários',
    'Cancel': 'Cancelar',
    'Cannot add time entry in previous timezone': 'Não é possível lançar horas em outro fuso horário',
    'Change': 'Alterar',
    'Click Here to Connect': 'Clique aqui para conectar',
    'Color Scheme': 'Esquema de cores',
    'Complete Sign up': 'Concluir cadastro',
    'Confirm': 'Confirmar',
    'Copy': 'Copiar',
    'Create New Goal': 'Criar meta',
    'Create New Integration': 'Criar integração',
    'Create something new': 'Criar algo novo',
    'Create To-Do': 'Criar tarefa',
    'Day': 'Dia',
    'Delete': 'Excluir',
    'Delete Article': 'Excluir documento',
    'Delete Key': 'Excluir chave',
    'Delete Project': 'Excluir projeto',
    'Details': 'Detalhes',
    'Did you know?': 'Você sabia?',
    "Don't map": 'Não mapear',
    'Draft': 'Rascunho',
    'Edit Key': 'Editar chave',
    'Edit Project': 'Editar projeto',
    'Editing': 'Editando',
    'Effort': 'Esforço',
    'Email': 'E-mail',
    'Enter: Save and close': 'Enter: salvar e fechar',
    'Events': 'Eventos',
    'Export': 'Exportar',
    'Filter': 'Filtro',
    'Finish the previous steps first': 'Conclua as etapas anteriores primeiro',
    'From (your integration)': 'De (sua integração)',
    "From here, we'll help you turn your task list into a project and goals. Then we'll work":
        'A partir daqui, vamos ajudar você a transformar sua lista de tarefas em um projeto com metas. Depois, vamos trabalhar',
    'together to identify your most important tasks so you can create some intentions':
        'juntos para identificar suas tarefas mais importantes e criar algumas intenções',
    'to get the work done.': 'para fazer o trabalho acontecer.',
    'Setting Intentions has been shown to': 'Definir intenções comprovadamente',
    'more than double the success rate': 'mais que dobra a taxa de sucesso',
    'of completing a task.': 'na conclusão de tarefas.',
    'Generate API Key': 'Gerar chave de API',
    'Go Back': 'Voltar',
    'Go back to integrations': 'Voltar às integrações',
    'Goal:': 'Meta:',
    'Group By': 'Agrupar por',
    'Hide': 'Ocultar',
    'Inherit': 'Herdar',
    'Integration Success': 'Integração concluída',
    'Integrations': 'Integrações',
    'Jump right back in': 'Continue de onde parou',
    'Keyboard shortcuts help': 'Ajuda dos atalhos de teclado',
    'List': 'Lista',
    'Loading activity...': 'Carregando atividade...',
    'Loading Subtasks ...': 'Carregando subtarefas...',
    'Loading...': 'Carregando...',
    'Match Fields': 'Associar campos',
    'Method not implemented': 'Método não implementado',
    'Metric:': 'Indicador:',
    'Milestone:': 'Marco:',
    'Miss': 'Não alcançada',
    'Month': 'Mês',
    'New Integration': 'Nova integração',
    'Next': 'Próximo',
    'No activity yet': 'Nenhuma atividade ainda',
    'No goals on this board yet. Open the': 'Ainda não há metas neste quadro. Abra o',
    'No tasks in this group.': 'Nenhuma tarefa neste grupo.',
    'None': 'Nenhum',
    'Not Available in this plan': 'Indisponível neste plano',
    'Nothing to see here. Move on.': 'Nada por aqui.',
    'of': 'de',
    'On Track': 'No prazo',
    'Open Project Hub': 'Abrir o hub de projetos',
    'Parent': 'Documento pai',
    'Password': 'Senha',
    'Please resolve the following errors and reconnect your integration:': 'Corrija os erros abaixo e reconecte a integração:',
    'Please review these requirements and make sure your import and mapping covers everything.':
        'Revise estes requisitos e confira se a importação e o mapeamento cobrem tudo.',
    'Press Enter to save and close. Press Shift plus Enter to save and add another task. Press Escape to cancel.':
        'Pressione Enter para salvar e fechar. Pressione Shift e Enter para salvar e adicionar outra tarefa. Pressione Esc para cancelar.',
    'Priority': 'Prioridade',
    'Project Checklist': 'Checklist do projeto',
    'Project Hub': 'Hub de projetos',
    'Project Type': 'Tipo de projeto',
    'Projects & Tasks': 'Projetos e tarefas',
    'Published': 'Publicado',
    'Remove': 'Remover',
    'Requirements for a successful import': 'Requisitos para uma importação bem-sucedida',
    'Reset Dashboard': 'Restaurar painel',
    'Resize to fit content': 'Ajustar ao conteúdo',
    'Review': 'Revisar',
    'Save': 'Salvar',
    'Secret:': 'Segredo:',
    'Select file': 'Selecionar arquivo',
    'Select my own': 'Escolher meus horários',
    'Shift+Enter: Save and add another': 'Shift+Enter: salvar e adicionar outra',
    'Show Closed Projects': 'Mostrar projetos encerrados',
    'Show Contents': 'Mostrar sumário',
    'Show Details': 'Mostrar detalhes',
    'Show Tasks': 'Mostrar tarefas',
    'Source Field': 'Campo de origem',
    'Start:': 'Início:',
    'Status breakdown': 'Distribuição por status',
    'Take me there': 'Ir para lá',
    'Task name': 'Nome da tarefa',
    'Telegram logo': 'Logo do Telegram',
    'Templates': 'Modelos',
    'The project checklist is list of activities you should do to ensure your projects are well defined, planned and executed.':
        'O checklist do projeto lista as atividades que garantem um projeto bem definido, planejado e executado.',
    'The quick brown fox jumps over the lazy dog': 'Um pequeno jabuti xereta viu dez cegonhas felizes',
    'The type of the project. This will determine which features are available.':
        'O tipo do projeto. Ele define quais recursos ficam disponíveis.',
    'Theme': 'Tema',
    'This entry was likely created using a different timezone. Only existing entries can be updated in this timezone':
        'Este lançamento provavelmente foi criado em outro fuso horário. Neste fuso, só é possível atualizar lançamentos existentes',
    'Ticket not found': 'Tarefa não encontrada',
    'To search type and hit enter...': 'Digite e pressione Enter para buscar...',
    'to start adding goals': 'para começar a adicionar metas',
    'today': 'hoje',
    'Type:': 'Tipo:',
    'unknown': 'desconhecido',
    'Upload CSV file': 'Enviar arquivo CSV',
    "We'll use these times to help prioritize your tasks": 'Vamos usar esses horários para ajudar a priorizar suas tarefas',
    'Week': 'Semana',
    'What are you importing?': 'O que você está importando?',
    'What are you working on? ↵': 'No que você está trabalhando? ↵',
    'What time do you usually start working?': 'A que horas você costuma começar a trabalhar?',
    'When do you normally end your work day? 🥳': 'Quando você costuma encerrar o dia de trabalho? 🥳',
    'When do you normally take a lunch break from work?': 'Quando você costuma fazer a pausa para o almoço?',
    'Year': 'Ano',
    "You don't have any favorites. 😿": 'Você ainda não tem favoritos. 😿',
    'Your API Key was successfully created. Please copy the key below. This is your only chance to copy it.':
        'Sua chave de API foi criada. Copie a chave abaixo — esta é a única oportunidade de copiá-la.',
    'Your data was synced successfully.': 'Seus dados foram sincronizados com sucesso.',
    'Your favorite color mode and scheme.': 'Seu modo e esquema de cores preferidos.',
    '⭐ My Favorites': '⭐ Meus favoritos',
    '🎨 Creating A Comfortable View': '🎨 Deixando a visualização confortável',
    '🗂️ All Assigned Projects': '🗂️ Todos os projetos atribuídos',
    '🗓️ Shaping A Daily Flow': '🗓️ Montando o ritmo do dia',
}

# Frases com expressões no meio: pares exatos por arquivo
MANUAL = {
    'app/Domain/Goalcanvas/Templates/dashboard.blade.php': [
        ('<h2>Progress: {{', '<h2>Progresso: {{'),
    ],
    'app/Domain/Reports/Templates/partials/needsAttention.blade.php': [
        ('maxPrecision: 1) }} of', 'maxPrecision: 1) }} de'),
    ],
    'app/Views/Templates/components/kanban/swimlane-row-header.blade.php': [
        ("{{ $totalCount }} tasks - {{ $expanded ? 'Expanded' : 'Collapsed' }}", "{{ $totalCount }} tarefas - {{ $expanded ? 'Expandido' : 'Recolhido' }}"),
        ('data-tippy-content="{{ $totalCount }} tasks"', 'data-tippy-content="{{ $totalCount }} tarefas"'),
    ],
    'app/Views/Templates/components/kanban/milestone-icon.blade.php': [
        ('"Milestone: {{ $label }}"', '"Marco: {{ $label }}"'),
    ],
    'app/Views/Templates/components/kanban/type-icon.blade.php': [
        ('"Type: {{ $label }}"', '"Tipo: {{ $label }}"'),
    ],
    'app/Domain/Tickets/Templates/showTicketModal.blade.php': [
        ('>Created by <?php', '>Criado por <?php'),
        ('?> | Last Updated: <?=', '?> | Última atualização: <?='),
    ],
    'app/Domain/Menu/Templates/headMenu.blade.php': [
        ('>Notification ({{ $totalNewNotifications }})</a>', '>Notificações ({{ $totalNewNotifications }})</a>'),
        ('>Mentions ({{ $totalNewMentions }})</a>', '>Menções ({{ $totalNewMentions }})</a>'),
    ],
}

PROTEGER = re.compile(r'<script\b.*?</script>|<style\b.*?</style>|@php.*?@endphp|\{\{--.*?--\}\}|\{\{.*?\}\}|\{!!.*?!!\}|<\?php.*?\?>|<\?=.*?\?>',
                      re.S | re.I)


def regioes_protegidas(s):
    return [(m.start(), m.end()) for m in PROTEGER.finditer(s)]


def protegido(pos, regioes):
    return any(a <= pos < b for a, b in regioes)


def traduzir_arquivo(s, textos):
    trocas = 0
    for en in sorted(set(textos), key=len, reverse=True):
        pt = TRAD.get(en)
        if not pt:
            continue
        regioes = regioes_protegidas(s)
        # Atributo com valor exato
        attr = re.compile(r'(?<![:\w-])((?:%s)\s*=\s*")%s(")' % ('|'.join(map(re.escape, ATRIBUTOS)), re.escape(en)))
        novo, n = attr.subn(lambda m: m.group(1) + pt + m.group(2), s)
        if n:
            s, trocas = novo, trocas + n
            regioes = regioes_protegidas(s)
        # Nó de texto inteiro
        corpo = r'\s+'.join(map(re.escape, en.split(' ')))
        for m in reversed(list(re.finditer(r'(?<![\w])' + corpo + r'(?![\w])', s))):
            if protegido(m.start(), regioes):
                continue
            antes = s[:m.start()].rstrip()
            depois = s[m.end():].lstrip()
            # Fronteira à esquerda: fim de tag/expressão, ou uma linha que é diretiva Blade (@if, @else…)
            ultima_linha = antes.rsplit('\n', 1)[-1].strip()
            fronteira = antes.endswith(('>', '}}', '!!}', '?>')) or bool(re.match(r'@\w+', ultima_linha))
            if fronteira and depois.startswith(('<', '{{', '{!!', '@')):
                s = s[:m.start()] + pt + s[m.end():]
                trocas += 1
    return s, trocas


def main():
    inventario = json.loads((TOOLS / 'inventario' / 'templates.json').read_text(encoding='utf-8'))
    total, sem_efeito = 0, []
    arquivos = set(inventario) | set(MANUAL)
    for rel in sorted(arquivos):
        if rel.startswith(PULAR):
            continue
        destino = OVERLAY / rel
        if not destino.exists():
            destino.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ORIGINAL / rel, destino)
        s = destino.read_text(encoding='utf-8')
        original = s
        for antigo, novo in MANUAL.get(rel, []):
            n = s.count(antigo)
            if n >= 1:
                s = s.replace(antigo, novo)  # trechos manuais são específicos: todas as ocorrências
            elif novo not in s:
                raise SystemExit(f'{rel}: trecho manual não encontrado: {antigo[:60]!r}')
        textos = [t for _, t in inventario.get(rel, [])]
        s, n = traduzir_arquivo(s, textos)
        for t in set(textos):
            if t in TRAD and TRAD[t] not in s and t in s:
                sem_efeito.append((rel, t))
        if s != original:
            destino.write_bytes(s.encode('utf-8'))
            total += 1
    print(f'arquivos alterados: {total}')
    if sem_efeito:
        print('sem efeito (revisar):')
        for rel, t in sem_efeito:
            print(f'  {rel}: {t[:70]!r}')


if __name__ == '__main__':
    main()
