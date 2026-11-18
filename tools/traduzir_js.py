"""Traduz para português os textos de interface nos bundles JS do Leantime 3.10.0.

- Pares exatos por bundle, sempre com o contexto (ex.: label:"Table"), nunca identificadores.
- Uppy (envio de arquivos): troca por chave só dentro dos blocos strings:{…}, inclusive plurais.
Copia o bundle original para o overlay se preciso. Idempotente.
Uso: python traduzir_js.py
"""
import re
import shutil
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
OVERLAY = TOOLS.parent / 'overlay'
ORIGINAL = Path(r'C:\Users\VLADSON\Downloads\Leantime-v3.10.0')
JS = 'public/dist/js/'

EDITOR = [
    # Menu "/" — rótulos
    ('label:"2 Columns"', 'label:"2 colunas"'), ('label:"3 Columns"', 'label:"3 colunas"'),
    ('label:"4 Columns"', 'label:"4 colunas"'), ('label:"Bullet List"', 'label:"Lista com marcadores"'),
    ('label:"Code Block"', 'label:"Bloco de código"'), ('label:"Collapsible"', 'label:"Seção recolhível"'),
    ('label:"Diagram"', 'label:"Diagrama"'), ('label:"Divider"', 'label:"Divisória"'),
    ('label:"Embed"', 'label:"Incorporar"'), ('label:"Heading 1"', 'label:"Título 1"'),
    ('label:"Heading 2"', 'label:"Título 2"'), ('label:"Heading 3"', 'label:"Título 3"'),
    ('label:"Image"', 'label:"Imagem"'), ('label:"Inline Math"', 'label:"Fórmula na linha"'),
    ('label:"Math Equation"', 'label:"Equação"'), ('label:"Numbered List"', 'label:"Lista numerada"'),
    ('label:"Quote"', 'label:"Citação"'), ('label:"Sidebar Both"', 'label:"Laterais dos dois lados"'),
    ('label:"Sidebar Left"', 'label:"Lateral à esquerda"'), ('label:"Sidebar Right"', 'label:"Lateral à direita"'),
    ('label:"Table"', 'label:"Tabela"'), ('label:"Table of Contents"', 'label:"Sumário"'),
    ('label:"Task List"', 'label:"Lista de verificação"'), ('label:"Template"', 'label:"Modelo"'),
    # Menu "/" — descrições
    ('description:"Add a blockquote"', 'description:"Adicionar uma citação"'),
    ('description:"Add a code snippet"', 'description:"Adicionar um trecho de código"'),
    ('description:"Add a horizontal divider"', 'description:"Adicionar uma linha divisória"'),
    ('description:"Add collapsible section"', 'description:"Adicionar uma seção recolhível"'),
    ('description:"Create a checklist with tasks"', 'description:"Criar uma lista de verificação"'),
    ('description:"Create a numbered list"', 'description:"Criar uma lista numerada"'),
    ('description:"Create a simple bullet list"', 'description:"Criar uma lista com marcadores"'),
    ('description:"Create four-column layout"', 'description:"Criar layout de quatro colunas"'),
    ('description:"Create three-column layout"', 'description:"Criar layout de três colunas"'),
    ('description:"Create two-column layout"', 'description:"Criar layout de duas colunas"'),
    ('description:"Embed video, docs, or other content"', 'description:"Incorporar vídeo, documentos ou outro conteúdo"'),
    ('description:"Insert a document template"', 'description:"Inserir um modelo de documento"'),
    ('description:"Insert a LaTeX math block"', 'description:"Inserir um bloco de fórmula LaTeX"'),
    ('description:"Insert a Mermaid diagram"', 'description:"Inserir um diagrama Mermaid"'),
    ('description:"Insert a table"', 'description:"Inserir uma tabela"'),
    ('description:"Insert an emoji"', 'description:"Inserir um emoji"'),
    ('description:"Insert auto-generated TOC"', 'description:"Inserir sumário automático"'),
    ('description:"Insert inline LaTeX formula"', 'description:"Inserir fórmula LaTeX na linha"'),
    ('description:"Large section heading"', 'description:"Título de seção grande"'),
    ('description:"Medium section heading"', 'description:"Título de seção médio"'),
    ('description:"Small section heading"', 'description:"Título de seção pequeno"'),
    ('description:"Narrow left, wide right layout"', 'description:"Esquerda estreita, direita larga"'),
    ('description:"Wide left, narrow right layout"', 'description:"Esquerda larga, direita estreita"'),
    ('description:"Sidebars on both sides of content"', 'description:"Colunas laterais dos dois lados"'),
    ('description:"Upload or embed an image"', 'description:"Enviar ou incorporar uma imagem"'),
    # Placeholders, prompts e textos
    ('placeholder:"Click to edit..."', 'placeholder:"Clique para editar..."'),
    ('placeholder:"Start writing your description..."', 'placeholder:"Comece a escrever a descrição..."'),
    ('placeholder:"Type \'/\' for commands or start writing..."', 'placeholder:"Digite \'/\' para comandos ou comece a escrever..."'),
    ('placeholder:"Write a comment..."', 'placeholder:"Escreva um comentário..."'),
    ('placeholder:"Write something …"', 'placeholder:"Escreva algo…"'),
    ('prompt("Edit LaTeX:"', 'prompt("Editar LaTeX:"'),
    ('prompt("Enter image URL:"', 'prompt("URL da imagem:"'),
    ('prompt("Enter LaTeX formula:"', 'prompt("Fórmula LaTeX:"'),
    ('text:"Click to expand"', 'text:"Clique para expandir"'),
]

BARRA = [
    ('setAttribute("aria-label","HTML source code")', 'setAttribute("aria-label","Código-fonte HTML")'),
    ('setAttribute("aria-label","Text formatting")', 'setAttribute("aria-label","Formatação de texto")'),
    ('label:"Align Center"', 'label:"Centralizar"'), ('label:"Align Left"', 'label:"Alinhar à esquerda"'),
    ('label:"Align Right"', 'label:"Alinhar à direita"'), ('label:"Clear Formatting"', 'label:"Limpar formatação"'),
    ('label:"Horizontal Line"', 'label:"Linha horizontal"'), ('label:"Subscript"', 'label:"Subscrito"'),
    ('label:"Superscript"', 'label:"Sobrescrito"'),
    ('prompt("Enter link text:"', 'prompt("Texto do link:"'), ('prompt("Enter URL:"', 'prompt("URL:"'),
    ('title:"Align Center"', 'title:"Centralizar"'), ('title:"Align Left"', 'title:"Alinhar à esquerda"'),
    ('title:"Align Right"', 'title:"Alinhar à direita"'), ('title:"Bold (Ctrl+B)"', 'title:"Negrito (Ctrl+B)"'),
    ('title:"Bullet List"', 'title:"Lista com marcadores"'), ('title:"Checklist"', 'title:"Lista de verificação"'),
    ('title:"Code Block"', 'title:"Bloco de código"'), ('title:"Edit HTML Source"', 'title:"Editar código HTML"'),
    ('title:"Font Family"', 'title:"Fonte"'), ('title:"Font Size"', 'title:"Tamanho da fonte"'),
    ('title:"Heading"', 'title:"Título"'), ('title:"Highlight"', 'title:"Destacar"'),
    ('title:"Image"', 'title:"Imagem"'), ('title:"Italic (Ctrl+I)"', 'title:"Itálico (Ctrl+I)"'),
    ('title:"More options"', 'title:"Mais opções"'), ('title:"Numbered List"', 'title:"Lista numerada"'),
    ('title:"Quote"', 'title:"Citação"'), ('title:"Redo (Ctrl+Shift+Z)"', 'title:"Refazer (Ctrl+Shift+Z)"'),
    ('title:"Strikethrough"', 'title:"Tachado"'), ('title:"Subscript"', 'title:"Subscrito"'),
    ('title:"Superscript"', 'title:"Sobrescrito"'), ('title:"Table"', 'title:"Tabela"'),
    ('title:"Text Color"', 'title:"Cor do texto"'), ('title:"Undo (Ctrl+Z)"', 'title:"Desfazer (Ctrl+Z)"'),
    # Paleta de cores e fontes (os nomes aparecem nos botões/dicas)
    ('{name:"Default",value:null}', '{name:"Padrão",value:null}'),
    ('{name:"Gray",value:', '{name:"Cinza",value:'), ('{name:"Red",value:', '{name:"Vermelho",value:'),
    ('{name:"Orange",value:', '{name:"Laranja",value:'), ('{name:"Yellow",value:', '{name:"Amarelo",value:'),
    ('{name:"Green",value:', '{name:"Verde",value:'), ('{name:"Blue",value:', '{name:"Azul",value:'),
    ('{name:"Purple",value:', '{name:"Roxo",value:'), ('{name:"Pink",value:', '{name:"Rosa",value:'),
    ('{name:"Small",value:"12px"}', '{name:"Pequeno",value:"12px"}'),
    ('{name:"Normal",value:null}', '{name:"Normal",value:null}'),
]

APP = [
    ('jQuery.growl({message:"To-Do Updated"', 'jQuery.growl({message:"Tarefa atualizada"'),
    ('replaceWith(" No due date")', 'replaceWith(" Sem prazo")'),
    ('labels:[t+"% Done",n+"% Open"]', 'labels:[t+"% concluído",n+"% em aberto"]'),
    ('{label:"Actual",', '{label:"Real",'),
    ('"aria-label":a||"Select date"', '"aria-label":a||"Selecionar data"'),
    ('"aria-label":"Choose date"', '"aria-label":"Escolher data"'),
    ('"aria-label":"Add new tag"', '"aria-label":"Adicionar etiqueta"'),
    # O rótulo e o replace que o remove precisam mudar juntos
    ('e.attr("aria-label","Empty column")', 'e.attr("aria-label","Coluna vazia")'),
    ('t.replace("Empty column","")', 't.replace("Coluna vazia","")'),
    ('"aria-label":"Task: "', '"aria-label":"Tarefa: "'),
    ('"You died :("', '"Fim de jogo :("'),
]

PLUGINS = [
    ('title:"Error!"', 'title:"Erro!"'), ('title:"Notice!"', 'title:"Aviso!"'),
    ('title:"Warning!"', 'title:"Atenção!"'), ('title:"Removing tag"', 'title:"Remover etiqueta"'),
]

GLOBAL = [
    ('e[0].label:"Close Tour"', 'e[0].label:"Fechar tour"'),
]

# Uppy: chave → texto (ou (singular, plural))
UPPY = {
    'addBulkFilesFailed': ('Falha ao adicionar %{smart_count} arquivo por erro interno', 'Falha ao adicionar %{smart_count} arquivos por erros internos'),
    'youCanOnlyUploadX': ('Você só pode enviar %{smart_count} arquivo', 'Você só pode enviar %{smart_count} arquivos'),
    'youHaveToAtLeastSelectX': ('Selecione pelo menos %{smart_count} arquivo', 'Selecione pelo menos %{smart_count} arquivos'),
    'exceedsSize': '%{file} ultrapassa o tamanho máximo permitido de %{size}',
    'missingRequiredMetaField': 'Faltam campos obrigatórios',
    'missingRequiredMetaFieldOnFile': 'Faltam campos obrigatórios em %{fileName}',
    'inferiorSize': 'Este arquivo é menor que o tamanho mínimo de %{size}',
    'youCanOnlyUploadFileTypes': 'Você só pode enviar: %{types}',
    'noMoreFilesAllowed': 'Não é possível adicionar mais arquivos',
    'noDuplicates': "Não é possível adicionar o arquivo duplicado '%{fileName}': ele já existe",
    'companionError': 'Falha na conexão com o Companion',
    'authAborted': 'Autenticação cancelada',
    'companionUnauthorizeHint': 'Para desautorizar sua conta %{provider}, acesse %{url}',
    'failedToUpload': 'Falha ao enviar %{file}',
    'noInternetConnection': 'Sem conexão com a internet',
    'connectedToInternet': 'Conectado à internet',
    'noFilesFound': 'Não há arquivos nem pastas aqui',
    'selectX': ('Selecionar %{smart_count}', 'Selecionar %{smart_count}'),
    'allFilesFromFolderNamed': 'Todos os arquivos da pasta %{name}',
    'openFolderNamed': 'Abrir a pasta %{name}',
    'cancel': 'Cancelar', 'logOut': 'Sair', 'filter': 'Filtrar', 'resetFilter': 'Limpar filtro',
    'loading': 'Carregando...',
    'authenticateWithTitle': 'Autentique-se no %{pluginName} para selecionar arquivos',
    'authenticateWith': 'Conectar ao %{pluginName}',
    'signInWithGoogle': 'Entrar com o Google',
    'searchImages': 'Buscar imagens',
    'enterTextToSearch': 'Digite o texto para buscar imagens',
    'search': 'Buscar',
    'emptyFolderAdded': 'Nenhum arquivo foi adicionado da pasta vazia',
    'folderAlreadyAdded': 'A pasta "%{folder}" já foi adicionada',
    'folderAdded': ('%{smart_count} arquivo adicionado de %{folder}', '%{smart_count} arquivos adicionados de %{folder}'),
    'uploading': 'Enviando', 'complete': 'Concluído', 'uploadFailed': 'Falha no envio', 'paused': 'Pausado',
    'retry': 'Tentar novamente', 'pause': 'Pausar', 'resume': 'Retomar', 'done': 'Concluído',
    'filesUploadedOfTotal': ('%{complete} de %{smart_count} arquivo enviado', '%{complete} de %{smart_count} arquivos enviados'),
    'dataUploadedOfTotal': '%{complete} de %{total}',
    'xTimeLeft': 'faltam %{time}',
    'uploadXFiles': ('Enviar %{smart_count} arquivo', 'Enviar %{smart_count} arquivos'),
    'uploadXNewFiles': ('Enviar +%{smart_count} arquivo', 'Enviar +%{smart_count} arquivos'),
    'upload': 'Enviar', 'retryUpload': 'Tentar enviar novamente',
    'xMoreFilesAdded': ('mais %{smart_count} arquivo adicionado', 'mais %{smart_count} arquivos adicionados'),
    'showErrorDetails': 'Mostrar detalhes do erro',
    'generatingThumbnails': 'Gerando miniaturas...',
    'closeModal': 'Fechar', 'addMoreFiles': 'Adicionar mais arquivos', 'addingMoreFiles': 'Adicionando mais arquivos',
    'importFrom': 'Importar de %{name}',
    'dashboardWindowTitle': 'Janela de envio de arquivos (Esc para fechar)',
    'dashboardTitle': 'Envio de arquivos',
    'copyLinkToClipboardSuccess': 'Link copiado.', 'copyLinkToClipboardFallback': 'Copie o endereço abaixo',
    'copyLink': 'Copiar link', 'back': 'Voltar', 'removeFile': 'Remover arquivo', 'editFile': 'Editar arquivo',
    'editing': 'Editando %{file}', 'finishEditingFile': 'Concluir edição', 'saveChanges': 'Salvar alterações',
    'myDevice': 'Meu dispositivo', 'dropHint': 'Solte os arquivos aqui', 'uploadComplete': 'Envio concluído',
    'uploadPaused': 'Envio pausado', 'resumeUpload': 'Retomar envio', 'pauseUpload': 'Pausar envio',
    'cancelUpload': 'Cancelar envio',
    'xFilesSelected': ('%{smart_count} arquivo selecionado', '%{smart_count} arquivos selecionados'),
    'uploadingXFiles': ('Enviando %{smart_count} arquivo', 'Enviando %{smart_count} arquivos'),
    'processingXFiles': ('Processando %{smart_count} arquivo', 'Processando %{smart_count} arquivos'),
    'poweredBy': 'Feito com %{uppy}',
    'addMore': 'Adicionar mais', 'editFileWithFilename': 'Editar o arquivo %{file}', 'save': 'Salvar',
    'dropPasteFiles': 'Solte os arquivos aqui ou %{browseFiles}',
    'dropPasteFolders': 'Solte os arquivos aqui ou %{browseFolders}',
    'dropPasteBoth': 'Solte os arquivos aqui, %{browseFiles} ou %{browseFolders}',
    'dropPasteImportFiles': 'Solte os arquivos aqui, %{browseFiles} ou importe de:',
    'dropPasteImportFolders': 'Solte os arquivos aqui, %{browseFolders} ou importe de:',
    'dropPasteImportBoth': 'Solte os arquivos aqui, %{browseFiles}, %{browseFolders} ou importe de:',
    'importFiles': 'Importar arquivos de:',
    'browseFiles': 'procure no computador', 'browseFolders': 'procure pastas',
    'recoveredXFiles': ('Não foi possível recuperar 1 arquivo. Selecione-o novamente e retome o envio.',
                        'Não foi possível recuperar %{smart_count} arquivos. Selecione-os novamente e retome o envio.'),
    'recoveredAllFiles': 'Todos os arquivos foram recuperados. Você já pode retomar o envio.',
    'sessionRestored': 'Sessão restaurada', 'reSelect': 'Selecionar novamente',
    'missingRequiredMetaFields': ('Falta um campo obrigatório: %{fields}.', 'Faltam campos obrigatórios: %{fields}.'),
    'takePictureBtn': 'Tirar foto', 'recordVideoBtn': 'Gravar vídeo',
    'dropHereOr': 'Solte aqui ou %{browse}', 'browse': 'procure',
    'chooseFiles': 'Escolher arquivos',
    'revert': 'Desfazer', 'rotate': 'Girar', 'zoomIn': 'Aumentar zoom', 'zoomOut': 'Diminuir zoom',
    'flipHorizontal': 'Espelhar', 'aspectRatioSquare': 'Recortar quadrado',
    'aspectRatioLandscape': 'Recortar paisagem (16:9)', 'aspectRatioPortrait': 'Recortar retrato (9:16)',
    'pluginNameAudio': 'Áudio', 'startAudioRecording': 'Iniciar gravação de áudio',
    'stopAudioRecording': 'Parar gravação de áudio', 'allowAudioAccessTitle': 'Permita o acesso ao microfone',
    'allowAudioAccessDescription': 'Para gravar áudio, permita o acesso ao microfone para este site.',
    'noAudioTitle': 'Microfone indisponível',
    'noAudioDescription': 'Para gravar áudio, conecte um microfone ou outro dispositivo de entrada de áudio',
    'recordingStoppedMaxSize': 'A gravação parou porque o arquivo está perto do tamanho máximo',
    'recordingLength': 'Duração da gravação %{recording_length}',
    'submitRecordedFile': 'Enviar gravação', 'discardRecordedFile': 'Descartar gravação',
    'import': 'Importar', 'enterUrlToImport': 'Informe a URL do arquivo a importar',
    'failedToFetch': 'O Companion não conseguiu acessar esta URL; confira se ela está correta',
    'enterCorrectUrl': 'URL incorreta: informe um link direto para o arquivo',
    'startCapturing': 'Iniciar captura de tela', 'stopCapturing': 'Parar captura de tela',
    'streamActive': 'Transmissão ativa', 'streamPassive': 'Transmissão pausada',
    'micDisabled': 'Acesso ao microfone negado pelo usuário', 'recording': 'Gravando',
    'pluginNameCamera': 'Câmera', 'noCameraTitle': 'Câmera indisponível',
    'noCameraDescription': 'Para tirar fotos ou gravar vídeo, conecte uma câmera',
    'smile': 'Sorria!', 'takePicture': 'Tirar uma foto', 'startRecording': 'Iniciar gravação de vídeo',
    'stopRecording': 'Parar gravação de vídeo', 'allowAccessTitle': 'Permita o acesso à câmera',
    'allowAccessDescription': 'Para tirar fotos ou gravar vídeo, permita o acesso à câmera para este site.',
    'timedOut': 'O envio parou por %{seconds} segundos e foi cancelado.',
    'creatingAssembly': 'Preparando envio...', 'creatingAssemblyFailed': 'Transloadit: não foi possível criar o Assembly',
    'encoding': 'Codificando...',
    'compressingImages': 'Comprimindo imagens...', 'compressedX': '%{size} economizados na compressão das imagens',
}

STR = r'(?:"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')'


def js_str(texto: str) -> str:
    """Literal JS entre aspas duplas (ou simples, se o texto tiver aspas duplas)."""
    if '"' in texto:
        return "'" + texto.replace("'", "\\'") + "'"
    return '"' + texto + '"'


def blocos_uppy(s: str):
    """Intervalos dos objetos strings:{…} (balanceados) que contêm textos."""
    for m in re.finditer(r'strings:\{', s):
        i, nivel = m.end(), 1
        while nivel and i < len(s):
            nivel += (s[i] == '{') - (s[i] == '}')
            i += 1
        yield m.start(), i


def traduzir_uppy(s: str) -> tuple[str, int]:
    trocas = 0
    partes, fim = [], 0
    for a, b in blocos_uppy(s):
        bloco = s[a:b]
        for chave, valor in UPPY.items():
            if isinstance(valor, tuple):
                rx = re.compile(r'(?<![\w$])%s:\{0:%s,1:%s\}' % (re.escape(chave), STR, STR))
                novo = '%s:{0:%s,1:%s}' % (chave, js_str(valor[0]), js_str(valor[1]))
            else:
                rx = re.compile(r'(?<![\w$])%s:%s' % (re.escape(chave), STR))
                novo = '%s:%s' % (chave, js_str(valor))
            bloco, n = rx.subn(lambda _m: novo, bloco)
            trocas += n
        partes.append(s[fim:a])
        partes.append(bloco)
        fim = b
    partes.append(s[fim:])
    return ''.join(partes), trocas


def aplicar(bundle: str, pares, uppy=False):
    rel = JS + bundle
    destino = OVERLAY / rel
    if not destino.exists():
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ORIGINAL / rel, destino)
    s = destino.read_text(encoding='utf-8')
    original = s
    for antigo, novo in pares:
        n = s.count(antigo)
        if n:
            s = s.replace(antigo, novo)
        elif novo not in s:
            raise SystemExit(f'{bundle}: trecho não encontrado: {antigo[:70]!r}')
    n_uppy = 0
    if uppy:
        s, n_uppy = traduzir_uppy(s)
    if s != original:
        destino.write_bytes(s.encode('utf-8'))
    print(f'{bundle}: {"alterado" if s != original else "sem mudanças"}' + (f' (Uppy: {n_uppy} textos)' if uppy else ''))


if __name__ == '__main__':
    aplicar('compiled-tiptap-editor.3.10.0.min.js', EDITOR)
    aplicar('compiled-tiptap-toolbar.3.10.0.min.js', BARRA)
    aplicar('compiled-app.3.10.0.min.js', APP)
    aplicar('compiled-framework-plugins.3.10.0.min.js', PLUGINS)
    aplicar('compiled-global-component.3.10.0.min.js', GLOBAL, uppy=True)
